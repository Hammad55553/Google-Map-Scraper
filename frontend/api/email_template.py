def get_email_template(body_content: str) -> str:
    """
    Wraps the email body content in a beautiful, modern HTML template.
    Includes a placeholder for a custom image.
    """
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* Base reset */
            body, p, h1, h2, h3, h4, h5, h6 {{
                margin: 0;
                padding: 0;
            }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f4f4f5;
                color: #333333;
                line-height: 1.6;
            }}
            .wrapper {{
                width: 100%;
                background-color: #f4f4f5;
                padding: 40px 0;
            }}
            .main-content {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }}
            /* Hero Image Area */
            .hero-image {{
                width: 100%;
                max-height: 300px;
                object-fit: cover;
                display: block;
                background-color: #1e293b;
            }}
            /* Header Area */
            .header {{
                background-color: #1e293b;
                padding: 24px;
                text-align: center;
                color: #ffffff;
            }}
            .header h1 {{
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
            /* Body Content */
            .content-body {{
                padding: 32px 24px;
                font-size: 16px;
                color: #334155;
            }}
            /* Styling for AI generated text elements */
            .content-body b, .content-body strong {{
                color: #0f172a;
                font-weight: 700;
            }}
            /* Footer */
            .footer {{
                background-color: #f8fafc;
                border-top: 1px solid #e2e8f0;
                padding: 24px;
                text-align: center;
                font-size: 13px;
                color: #64748b;
            }}
            .footer a {{
                color: #3b82f6;
                text-decoration: none;
            }}
            /* Responsive */
            @media screen and (max-width: 600px) {{
                .wrapper {{
                    padding: 10px;
                }}
                .main-content {{
                    width: 100%;
                }}
                .content-body {{
                    padding: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="main-content">
                
                <!-- AAP APNI POST KI IMAGE YAHAN ADD KAREIN -->
                <!-- src="" ke andar apne image ka direct link daal dain (jaise https://example.com/my-post.jpg) -->
                <!-- Agar image na lagani ho to is line ko delete kar dain -->
                <img src="https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?auto=format&fit=crop&q=80&w=600&h=200" alt="Cover Image" class="hero-image">
                
                <!-- Header (Optional) -->
                <!-- <div class="header">
                    <h1>Your Custom Title</h1>
                </div> -->

                <!-- Main Email Text -->
                <div class="content-body">
                    {body_content}
                </div>

                <!-- Footer -->
                <div class="footer">
                    <p>Sent via Professional Outreach</p>
                    <p>Contact: <a href="mailto:asperinfotech@gmail.com">asperinfotech@gmail.com</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
