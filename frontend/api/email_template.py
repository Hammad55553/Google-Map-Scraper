def get_email_template(body_content: str, image_url: str = "", top_body_content: str = "") -> str:
    """
    Wraps the email body content in a beautiful, modern HTML template.
    Includes a placeholder for a custom image.
    """
    
    image_tag = ""
    if image_url:
        image_tag = f'<img src="{image_url}" alt="Cover Image" class="hero-image">'
        
    top_body_tag = ""
    if top_body_content:
        top_body_tag = f'<div class="content-body top-body">{top_body_content}</div>'

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
                height: auto;
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
            .top-body {{
                padding-bottom: 0px !important;
                margin-bottom: 20px;
            }}
            /* Styling for AI generated text elements */
            .content-body b, .content-body strong {{
                color: #0f172a;
                font-weight: 700;
            }}
            /* Footer */
            .footer {{
                background-color: #0c527c;
                padding: 40px 24px;
                text-align: center;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }}
            .social-icons {{
                margin-bottom: 30px;
            }}
            .social-icons a {{
                display: inline-block;
                margin: 0 10px;
                text-decoration: none;
            }}
            .social-icons img {{
                width: 20px;
                height: 20px;
            }}
            .footer-address {{
                margin-bottom: 15px;
                font-size: 14px;
            }}
            .footer-links {{
                font-size: 14px;
                font-weight: bold;
            }}
            .footer-links a {{
                color: #3b9cdb;
                text-decoration: underline;
                margin: 0 5px;
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
                .social-icons a {{
                    margin: 0 5px;
                }}
                .social-icons img {{
                    width: 18px;
                    height: 18px;
                }}
                .footer {{
                    padding: 30px 15px;
                }}
                .footer-address {{
                    font-size: 12px;
                }}
                .footer-links {{
                    font-size: 12px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="main-content">
                
                <!-- Top Text Section -->
                {top_body_tag}
                
                <!-- Image Section -->
                {image_tag}
                
                <!-- Main Email Text -->
                <div class="content-body">
                    {body_content}
                </div>

                <!-- Footer -->
                <div class="footer">
                    <img src="https://asperinfotech.vercel.app/unnamed.png" alt="Asper Infotech" style="max-height: 50px; margin-bottom: 15px;">
                    <div class="social-icons">
                        <a href="https://youtube.com/@asperinfotech" target="_blank"><img src="https://img.icons8.com/ios-filled/50/ffffff/youtube-play.png" alt="YouTube"></a>
                        <a href="https://www.facebook.com/AsperInfoTech" target="_blank"><img src="https://img.icons8.com/ios-filled/50/ffffff/facebook-new.png" alt="Facebook"></a>
                        <a href="https://www.linkedin.com/company/asperinfotech/" target="_blank"><img src="https://img.icons8.com/ios-filled/50/ffffff/linkedin.png" alt="LinkedIn"></a>
                        <a href="https://www.instagram.com/asperinfotech" target="_blank"><img src="https://img.icons8.com/ios-filled/50/ffffff/instagram-new.png" alt="Instagram"></a>
                        <a href="https://tiktok.com/@asperinfotech/" target="_blank"><img src="https://img.icons8.com/ios-filled/50/ffffff/tiktok.png" alt="TikTok"></a>
                        <a href="https://x.com/AsperInfoTech" target="_blank"><img src="https://img.icons8.com/ios-filled/50/ffffff/x.png" alt="X"></a>
                    </div>
                    
                    <div class="footer-address">
                        Asper Infotech Private Limited, Quaid-E-Azam Colony Hasilpur, Pakistan
                    </div>
                    
                    <div class="footer-links">
                        <a href="https://asperinfotech.vercel.app/#" target="_blank">Unsubscribe (Coming Soon)</a> &nbsp;|&nbsp; <a href="https://asperinfotech.vercel.app/contact" target="_blank">Contact Us</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
