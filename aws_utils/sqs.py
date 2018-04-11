class Sqs:
    def __init__(self, session):
        self.client = session.client('sqs')

    def __call__(self, queue_url):
        self.queue_url = self.client.get_queue_url(QueueName=queue_url)['QueueUrl']
        return self

    def send_message(self, **kwargs):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            **kwargs
        )
        return response

    def send_message_batch(self, entries):
        response = self.client.send_message_batch(
            QueueUrl=self.queue_url,
            Entries=entries
        )
        return response
