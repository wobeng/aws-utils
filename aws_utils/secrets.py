import json


class Secrets:
    def __init__(self, session):
        self.client = session.client('secretsmanager')

    def parameter(self, name):
        response = self.client.get_secret_value(SecretId=name)
        return json.loads(response['SecretString'])
