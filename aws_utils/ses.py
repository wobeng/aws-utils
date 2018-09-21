import traceback
from json import dumps


class Ses:
    def __init__(self, session):
        self.client = session.client('ses')

    def send_email(self, from_email, to_email, subject, message):
        self.client.send_email(
            Source=from_email,
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': message}}
            }
        )

    def send_exception_email(self, email, domain, event):
        message = dumps(event) + '\n' + traceback.format_exc().replace('\n', '<br /><br />')
        subject = 'Error occurred in ' + domain
        self.send_email(email, email, subject, message)
