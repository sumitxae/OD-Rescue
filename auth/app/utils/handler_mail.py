from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config.config import Config
from fastapi import HTTPException

class MailHandler:
    def __init__(self, api_key=Config.SENDGRID_API_KEY):
        """
        Initialize the MailHandler with SendGrid API Key.
        """
        import os
        import certifi

        os.environ['SSL_CERT_FILE'] = certifi.where()
        self.api_key = api_key or Config.SENDGRID_API_KEY
        self.client = SendGridAPIClient(self.api_key)

    def send_email(self, to_email: str, subject: str, content: str):
        """
        Send an email using SendGrid.

        Args:
            to_email (str): Recipient's email address.
            subject (str): Email subject.
            content (str): Email body (HTML or plain text).

        Returns:
            dict: Response message.
        """
        try:
            message = Mail(
                from_email=Config.SENDER_EMAIL,  # Configure in your config file
                to_emails=to_email,
                subject=subject,
                html_content=content,
            )

            response = self.client.send(message)
            return {"status": response.status_code, "message": "Email sent successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
