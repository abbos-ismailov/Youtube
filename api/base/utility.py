from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import threading
import re
regex_username = '^[a-z0-9_-]{3,20}$'

############################################################ Email sending message with thread
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self=self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"], body=data["body"], to=[data["to_email"]]
        )
        if data.get("content_type") == "html":
            email.content_subtype = "html"

        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string("auth/send_email_code.html", {"code": code})
    Email.send_email(
        {
            "subject": "Youtubedan ro'yhatdan o'tish",
            "body": html_content,
            "to_email": email,
            "content_type": "html",
        }
    )
############################################################


def check_username(username):
    if re.fullmatch(regex_username, username):
        return True
    else:
        return False