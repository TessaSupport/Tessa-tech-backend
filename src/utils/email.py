import logging
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from tenacity import retry, stop_after_attempt, wait_exponential
from postmarker.core import PostmarkClient
from utils.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self) -> None:
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"])
        )

        # Default sender configuration
        self.default_sender = settings.DEFAULT_FROM_EMAIL

        # Postmark client
        self.client = PostmarkClient(server_token=settings.POSTMARK_API_TOKEN)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def send_template_email(
        self,
        to: str,
        subject: str,
        template_name: str,
        template_data: Dict[str, Any]
    ) -> bool:
        """
        Send an email using Postmark with a rendered Jinja2 template
        """
        try:
            html_content = self._render_template(template_name, template_data)

            response = self.client.emails.send(
                From=self.default_sender,
                To=to,
                Subject=subject,
                HtmlBody=html_content,
                MessageStream="outbound",
                TrackOpens=True
            )

            logger.info(
                "Email sent successfully",
                extra={
                    "to": to,
                    "template": template_name,
                    "message_id": response["MessageID"]
                }
            )
            return True

        except Exception as e:
            logger.error(
                "Failed to send email",
                exc_info=e,
                extra={"to": to, "template": template_name}
            )
            if not settings.DEBUG:
                raise
            return False

    def send_otp_email(self, to: str, username: str, otp: str) -> bool:
        return self.send_template_email(
            to=to,
            subject="Verify Your Email - Tessa",
            template_name="verify",
            template_data={"username": username, "otp": otp}
        )

    def send_welcome_email(self, to: str, username: str) -> bool:
        return self.send_template_email(
            to=to,
            subject="Welcome to Tessa!",
            template_name="welcome",
            template_data={"username": username}
        )

    def send_subscription_success_email(
        self, to: str, username: str, subscription_details: Dict[str, Any] = None
    ) -> bool:
        data = {"username": username}
        if subscription_details:
            data.update(subscription_details)

        return self.send_template_email(
            to=to,
            subject="Subscription Successful - Tessa",
            template_name="subscription_success",
            template_data=data
        )

    def send_agent_invite_email(
        self, to: str, username: str, invite_data: Dict[str, Any] = None
    ) -> bool:
        data = {"username": username}
        if invite_data:
            data.update(invite_data)

        return self.send_template_email(
            to=to,
            subject="Agent Invitation - Tessa",
            template_name="agentinvite",
            template_data=data
        )

    def _render_template(self, template_name: str, template_data: Dict[str, Any]) -> str:
        try:
            template = self.jinja_env.get_template(f"{template_name}.html")
            return template.render(**template_data)
        except Exception as e:
            logger.error(
                "Template rendering failed",
                exc_info=e,
                extra={"template": template_name}
            )
            raise


# Singleton instance
email_service = EmailService()


# # Legacy wrapper functions (backward compatibility)
# def send_email(to: str, subject: str, body: str):
#     return email_service.send_template_email(
#         to=to,
#         subject=subject,
#         template_name="plain_text",
#         template_data={"body": body}
#     )


def send_otp_email(to: str, username: str, otp: str):
    return email_service.send_otp_email(to, username, otp)


def send_welcome_email(to: str, username: str):
    return email_service.send_welcome_email(to, username)


def send_subscription_success_email(to: str, username: str, subscription_details: dict = None):
    return email_service.send_subscription_success_email(to, username, subscription_details)


def send_agent_invite_email(to: str, username: str, invite_data: dict = None):
    return email_service.send_agent_invite_email(to, username, invite_data)
