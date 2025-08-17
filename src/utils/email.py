import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils.config import settings

class EmailService:
    def __init__(self):
        # Use config settings instead of direct env vars
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
    def send_template_email(self, to: str, subject: str, template_name: str, template_data: dict):
        """
        Send email using Jinja2 HTML template with dynamic data
        """
        try:
            # Render template with Jinja2
            html_content = self.render_template(template_name, template_data)
            
            # Check if SMTP credentials are available
            if not self.smtp_username or not self.smtp_password:
                print(f"[INFO] SMTP not configured. Email would be sent to {to}:")
                print(f"[INFO] Subject: {subject}")
                print(f"[INFO] Template: {template_name}")
                print(f"[INFO] OTP: {template_data.get('otp', 'N/A')}")
                return True
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_username
            msg['To'] = to
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            print(f"[SUCCESS] {template_name} email sent to {to}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send {template_name} email: {e}")
            print(f"[FALLBACK] Email would be sent to {to}:")
            print(f"[FALLBACK] Subject: {subject}")
            print(f"[FALLBACK] Template: {template_name}")
            print(f"[FALLBACK] OTP: {template_data.get('otp', 'N/A')}")
            print(f"[FALLBACK] HTML Content: {html_content[:200]}...")
            return False
    
    def render_template(self, template_name: str, template_data: dict) -> str:
        """
        Render HTML template with Jinja2
        """
        try:
            template = self.jinja_env.get_template(f"{template_name}.html")
            return template.render(**template_data)
        except Exception as e:
            print(f"[ERROR] Template rendering failed: {e}")
            # Fallback to simple HTML
            return self._fallback_html(template_name, template_data)
    
    def _fallback_html(self, template_name: str, data: dict) -> str:
        """
        Fallback HTML if template rendering fails
        """
        if template_name == "verify":  # Match your actual template name
            return f"""
            <html>
                <body>
                    <h2>Verify Your Email</h2>
                    <p>Hello {data.get('username', 'User')},</p>
                    <p>Your verification code is: <strong>{data.get('otp', '')}</strong></p>
                    <p>This code expires in 10 minutes.</p>
                </body>
            </html>
            """
        elif template_name == "welcome":
            return f"""
            <html>
                <body>
                    <h2>Welcome to Tessa!</h2>
                    <p>Hello {data.get('username', 'User')},</p>
                    <p>Your account has been successfully verified!</p>
                </body>
            </html>
            """
        else:
            return f"<html><body><p>Email content for {template_name}</p></body></html>"

# Global email service instance
email_service = EmailService()

def send_email(to: str, subject: str, body: str):
    """
    Legacy function for backward compatibility
    """
    return email_service.send_template_email(to, subject, "plain_text", {"body": body})

def send_otp_email(to: str, username: str, otp: str):
    """
    Send OTP verification email with Jinja2 template
    """
    return email_service.send_template_email(
        to=to,
        subject="Verify Your Email - Tessa",
        template_name="verify",  # Updated to match your template name
        template_data={"username": username, "otp": otp}
    )

def send_welcome_email(to: str, username: str):
    """
    Send welcome email with Jinja2 template
    """
    return email_service.send_template_email(
        to=to,
        subject="Welcome to Tessa!",
        template_name="welcome",  # Updated to match your template name
        template_data={"username": username}
    )

def send_subscription_success_email(to: str, username: str, subscription_details: dict = None):
    """
    Send subscription success email with Jinja2 template
    """
    data = {"username": username}
    if subscription_details:
        data.update(subscription_details)
    
    return email_service.send_template_email(
        to=to,
        subject="Subscription Successful - Tessa",
        template_name="subscription_success",
        template_data=data
    )

def send_agent_invite_email(to: str, username: str, invite_data: dict = None):
    """
    Send agent invitation email with Jinja2 template
    """
    data = {"username": username}
    if invite_data:
        data.update(invite_data)
    
    return email_service.send_template_email(
        to=to,
        subject="Agent Invitation - Tessa",
        template_name="agentinvite",  # Updated to match your template name
        template_data=data
    )
