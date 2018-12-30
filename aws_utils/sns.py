import traceback
from io import StringIO

from simplejson import dumps


class Sns:
    def __init__(self, session):
        self.client = session.client('sns')
        self.account_id = session.client('sts').get_caller_identity()['Account']
        self.region_name = session.region_name

    def __call__(self, group_name=None, region_name=None):
        if group_name:
            self.group_name = group_name
        if region_name:
            self.region_name = region_name
        return self

    def publish(self, subject, message):
        topic_arn = 'arn:aws:sns:{}:{}:{}'.format(self.region_name, self.account_id, self.group_name)
        self.client.publish(TopicArn=topic_arn, Message=message, Subject=subject)

    def send_exception_email(self, domain, event):
        fp = StringIO(dumps(event) + ' \n')
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        subject = 'Error occurred in ' + domain
        self.publish(subject, message)
