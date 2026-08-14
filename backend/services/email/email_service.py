# ==========================================================
# PDF MASTER AI
# Email Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import smtplib

from email.message import EmailMessage

from core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD
)

from core.logger import info


# ----------------------------------------------------------
# EMAIL SERVICE
# ----------------------------------------------------------

class EmailService:

    """
    Email Service.

    Handles outgoing application emails.
    """

    # ------------------------------------------------------
    # INITIALIZE
    # ------------------------------------------------------

    def __init__(self):

        self.smtp_server = SMTP_SERVER

        self.smtp_port = int(
            SMTP_PORT or 587
        )

        self.username = SMTP_USERNAME

        self.password = SMTP_PASSWORD


    # ------------------------------------------------------
    # SEND EMAIL
    # ------------------------------------------------------

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str
    ) -> bool:

        """
        Send plain text email.
        """

        if not self.smtp_server:

            raise ValueError(
                "SMTP_SERVER is not configured."
            )

        if not self.username:

            raise ValueError(
                "SMTP_USERNAME is not configured."
            )

        if not self.password:

            raise ValueError(
                "SMTP_PASSWORD is not configured."
            )


        message = EmailMessage()

        message["Subject"] = subject

        message["From"] = self.username

        message["To"] = to_email

        message.set_content(
            body
        )


        with smtplib.SMTP(
            self.smtp_server,
            self.smtp_port
        ) as server:

            server.starttls()

            server.login(
                self.username,
                self.password
            )

            server.send_message(
                message
            )


        info(
            f"Email sent successfully: {to_email}"
        )

        return True


    # ------------------------------------------------------
    # SEND PASSWORD RESET EMAIL
    # ------------------------------------------------------

    def send_password_reset_email(
        self,
        to_email: str,
        reset_url: str
    ) -> bool:

        """
        Send password reset email.
        """

        subject = (
            "Reset Password - PDF Master AI"
        )


        body = f"""
PDF Master AI

Halo,

Kami menerima permintaan untuk mengatur
ulang password akun PDF Master AI kamu.

Klik link berikut untuk membuat password baru:

{reset_url}

Link ini hanya berlaku selama 30 menit.

Jika kamu tidak meminta reset password,
abaikan email ini.

Salam,

PDF Master AI
"""


        return self.send_email(
            to_email=to_email,
            subject=subject,
            body=body
        )