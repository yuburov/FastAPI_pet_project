import abc
import smtplib
from email.message import EmailMessage

from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


class AbstractNotifications(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, subject, message):
        raise NotImplementedError


class EmailNotifications(AbstractNotifications):
    def __init__(self, smtp_host=SMTP_HOST, port=SMTP_PORT):
        self.smtp_host = smtp_host
        self.smtp_port = port

    def send(self, destination, subject, message):
        msg = EmailMessage()
        msg.set_content(message)
        msg['From'] = SMTP_USER
        msg['To'] = destination
        msg['Subject'] = subject

        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
