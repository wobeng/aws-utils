import json
from os import environ


class Secrets:
    def __init__(self, session):
        self.client = session.client('secretsmanager')

    def load(self, name):
        response = self.client.get_secret_value(SecretId=name)
        secrets = json.loads(response['SecretString'])
        for name, secret in secrets.items():
            environ[name] = secret
