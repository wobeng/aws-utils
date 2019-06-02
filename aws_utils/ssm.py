import os


class Ssm:
    def __init__(self, session):
        self.client = session.client('ssm')
        self.db = session.client('dynamodb')

    def parameter(self, name, default=None):
        name = str(name)
        return os.environ.get(name, default)
