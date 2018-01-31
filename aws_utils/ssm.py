import os


class Ssm:
    def __init__(self, session):
        self.client = session.client('ssm')

    def parameter(self, name):
        value = os.environ.get(name, None)
        if not value:
            value = self.client.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']
            os.environ[name] = value
        return value
