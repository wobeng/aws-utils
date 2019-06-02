import os


class Ssm:
    def __init__(self, session):
        self.client = session.client('ssm')

    def parameter(self, name, default=None):
        name = str(name)
        return os.environ.get(name, default)
