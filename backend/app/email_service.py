"""Email service for sending booking notifications."""

import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "neerupudijohnsonnj@gmail.com")


async def send_booking_email(booking_data: dict):
    """Send booking notification email.
    
    Args:
        booking_data: Dictionary containing booking information
    """
    # Create email message
    message = MIMEMultipart("alternative")
    message["Subject"] = f"New Booking: {booking_data['service']} - {booking_data['name']}"
    message["From"] = SMTP_USER or "noreply@godavaricaptures.com"
    message["To"] = RECIPIENT_EMAIL
    
    # Create HTML email body
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                <h2 style="color: #D4AF37; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">
                    New Booking Received
                </h2>
                
                <div style="margin: 20px 0;">
                    <h3 style="color: #555;">Customer Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; font-weight: bold; width: 150px;">Name:</td>
                            <td style="padding: 8px;">{booking_data['name']}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="padding: 8px; font-weight: bold;">Phone:</td>
                            <td style="padding: 8px;">{booking_data['phone']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold;">Service:</td>
                            <td style="padding: 8px;">{booking_data['service']}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="padding: 8px; font-weight: bold;">Event Date:</td>
                            <td style="padding: 8px;">{booking_data['event_date']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold;">Location:</td>
                            <td style="padding: 8px;">{booking_data['location']}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="padding: 8px; font-weight: bold;">Message:</td>
                            <td style="padding: 8px;">{booking_data['message'] or 'No message provided'}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold;">Booking ID:</td>
                            <td style="padding: 8px; font-size: 12px; color: #666;">{booking_data['id']}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="padding: 8px; font-weight: bold;">Received At:</td>
                            <td style="padding: 8px;">{booking_data['created_at']}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="margin-top: 30px; padding: 15px; background-color: #f0f0f0; border-left: 4px solid #D4AF37;">
                    <p style="margin: 0; font-size: 14px; color: #666;">
                        This is an automated notification from Godavari Captures booking system.
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    
    # Create plain text version
    text_body = f"""
    New Booking Received - Godavari Captures
    
    Customer Details:
    -----------------
    Name: {booking_data['name']}
    Phone: {booking_data['phone']}
    Service: {booking_data['service']}
    Event Date: {booking_data['event_date']}
    Location: {booking_data['location']}
    Message: {booking_data['message'] or 'No message provided'}
    
    Booking ID: {booking_data['id']}
    Received At: {booking_data['created_at']}
    
    ---
    This is an automated notification from Godavari Captures booking system.
    """
    
    # Attach both HTML and plain text versions
    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    try:
        if SMTP_USER and SMTP_PASSWORD:
            # Use configured SMTP server
            await aiosmtplib.send(
                message,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                start_tls=True,
            )
            print(f"✅ Booking email sent to {RECIPIENT_EMAIL}")
        else:
            # Log to console if SMTP not configured
            print("⚠️ SMTP not configured. Email would be sent to:", RECIPIENT_EMAIL)
            print("📧 Email content:")
            print(text_body)
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        # Don't raise exception - booking should still succeed even if email fails
