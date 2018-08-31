from simplejson import dumps


class Sqs:
    def __init__(self, session):
        self.client = session.client('sqs')

    def __call__(self, queue_name):
        self.queue_url = self.client.get_queue_url(QueueName=queue_name)['QueueUrl']
        return self

    def send_message(self, message, **kwargs):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=dumps(message, use_decimal=True),
            **kwargs
        )
        return response

    def send_message_batch(self, entries):

        n = 10
        new_entries = [entries[i * n:(i + 1) * n] for i in range((len(entries) + n - 1) // n)]

        for ne in new_entries:
            ne_copy = ne.copy()
            get_out = False
            while not get_out:
                response = self.client.send_message_batch(
                    QueueUrl=self.queue_url,
                    Entries=ne_copy
                )
                if response.get('Failed', None):
                    failed_ids = [f['Id'] for f in response['Failed']]
                    ne_copy = [e for e in ne if e['Id'] in failed_ids]
                else:
                    get_out = True
