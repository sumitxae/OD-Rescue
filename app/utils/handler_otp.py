from .handler_cache import InMemoryOTPStore
from .handler_mail import MailHandler
import logging

logger = logging.getLogger(__name__)
mail_handler = MailHandler()

class OtpHandler:
    """
    A class to handle OTP (One Time Password) generation and validation.
    """

    def __init__(self, otp_length=6):
        self.otp_length = otp_length


    def generate_otp(self):
        """
        Generate a random OTP of specified length.
        """
        import random
        import string

        digits = string.digits
        otp = ''.join(random.choice(digits) for _ in range(self.otp_length))
        return otp

    async def send_otp(self, email: str) -> bool:
        """
        Generate and send OTP to the given email.
        """
        otp = self.generate_otp()
        InMemoryOTPStore.set(email, otp, ttl=300)  # 5 min TTL

        # Replace with actual SendGrid email sending
        try:
            mail_handler.send_email(to_email=email, subject="Your OTP", content=f"Your OTP is {otp}")
            logger.info(f"Sent OTP {otp} to {email}")  # replace with actual logging
            return True
        except Exception as e:
            logger.error(f"Failed to send OTP to {email}: {str(e)}")
            return False

    @staticmethod
    def verify_otp(email: str, otp: str) -> bool:
        """
        Verify the OTP sent to the user.
        """
        stored_otp = InMemoryOTPStore.get(email)
        if stored_otp and stored_otp == otp:
            InMemoryOTPStore.delete(email)
            return True
        return False