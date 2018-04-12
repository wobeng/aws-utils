from simplejson import dumps


class Swf:
    def __init__(self, session):
        self.client = session.client('swf')

    def __call__(self, queue_url):
        self.queue_url = self.client.get_queue_url(QueueName=queue_url)['QueueUrl']
        return self

    def start_workflow_execution(self, domain, meta_data, **kwargs):
        response = self.client.start_workflow_execution(
            domain=domain,
            input=dumps(meta_data, use_decimal=True),
            **kwargs
        )
        return response
