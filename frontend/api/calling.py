import os
import json
import asyncio
import websockets
from fastapi import APIRouter, WebSocket, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, PlainTextResponse
from twilio.rest import Client
import base64

router = APIRouter()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DOMAIN = os.getenv("DOMAIN", "localhost:8000") # Important for webhook URL

# In-memory store for active call pitches
call_pitches = {}

@router.post("/api/calls/outbound")
async def start_outbound_call(request: Request):
    data = await request.json()
    phone = data.get("phone")
    pitch = data.get("pitch")
    
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OPENAI_API_KEY]):
        return {"error": "Missing Twilio or OpenAI credentials in environment variables"}
        
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    # We use a Twilio TwiML Bin or dynamically generate TwiML to connect to the Stream
    twiml = f"""
    <Response>
        <Connect>
            <Stream url="wss://{DOMAIN}/api/calls/media" />
        </Connect>
    </Response>
    """
    
    call = client.calls.create(
        twiml=twiml,
        to=phone,
        from_=TWILIO_PHONE_NUMBER
    )
    
    # Store pitch for this call SID
    call_pitches[call.sid] = pitch
    return {"status": "Call initiated", "call_sid": call.sid}

@router.websocket("/api/calls/media")
async def handle_media_stream(websocket: WebSocket):
    await websocket.accept()
    
    # We need to bridge Twilio WebSocket <-> OpenAI WebSocket
    openai_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    try:
        async with websockets.connect(openai_url, additional_headers=headers) as openai_ws:
            # First, send session update to configure audio formats (Twilio uses g711_ulaw at 8000Hz)
            session_update = {
                "type": "session.update",
                "session": {
                    "turn_detection": {"type": "server_vad"},
                    "input_audio_format": "g711_ulaw",
                    "output_audio_format": "g711_ulaw",
                    "voice": "alloy",
                    "instructions": "You are a professional B2B sales assistant. Keep your responses concise, natural, and persuasive. Speak as if you are on a phone call. If asked a question, answer it. Pitch: We help businesses improve their Google Maps presence.",
                    "modalities": ["text", "audio"],
                    "temperature": 0.7,
                }
            }
            await openai_ws.send(json.dumps(session_update))

            stream_sid = None

            async def receive_from_twilio():
                nonlocal stream_sid
                try:
                    while True:
                        message = await websocket.receive_text()
                        packet = json.loads(message)
                        
                        if packet['event'] == 'start':
                            stream_sid = packet['start']['streamSid']
                            call_sid = packet['start']['callSid']
                            pitch = call_pitches.get(call_sid, "")
                            
                            if pitch:
                                # Update instructions with actual pitch
                                await openai_ws.send(json.dumps({
                                    "type": "session.update",
                                    "session": {
                                        "instructions": f"You are a B2B sales assistant. Pitch this naturally: {pitch}"
                                    }
                                }))
                                
                            # Trigger the AI to say hello
                            await openai_ws.send(json.dumps({
                                "type": "response.create",
                                "response": {
                                    "modalities": ["text", "audio"],
                                    "instructions": "Say hello and start the pitch."
                                }
                            }))
                            
                        elif packet['event'] == 'media':
                            # Forward audio to OpenAI
                            audio_payload = packet['media']['payload']
                            await openai_ws.send(json.dumps({
                                "type": "input_audio_buffer.append",
                                "audio": audio_payload
                            }))
                            
                        elif packet['event'] == 'stop':
                            break
                except Exception as e:
                    print(f"Twilio receive error: {e}")

            async def receive_from_openai():
                try:
                    async for openai_message in openai_ws:
                        response = json.loads(openai_message)
                        
                        if response['type'] == 'response.audio.delta' and response.get('delta'):
                            # Send audio back to Twilio
                            audio_payload = response['delta']
                            if stream_sid:
                                await websocket.send_json({
                                    "event": "media",
                                    "streamSid": stream_sid,
                                    "media": {
                                        "payload": audio_payload
                                    }
                                })
                except Exception as e:
                    print(f"OpenAI receive error: {e}")

            # Run both listeners concurrently
            await asyncio.gather(receive_from_twilio(), receive_from_openai())
            
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
