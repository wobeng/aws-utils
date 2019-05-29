import os


class Ssm:
    def __init__(self, session):
        self.client = session.client('ssm')
        self.db = session.client('dynamodb')

    def parameter(self, name, default=None):
        name = str(name)
        value = os.environ.get(name, default)
        if not value:
            try:
                value = self.client.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']
                os.environ[name] = value
            except BaseException as e:
                print(name, e)
        self.db.put_item(
            TableName='Vars',
            Item={
                'vars': {
                    'S': value,
                }}
        )
        return value
