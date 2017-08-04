import json


class Lambda:
    def __init__(self, session):
        self.client = session.client("lambda")

    def invoke(self, function_name, payload):
        response = self.client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        return response["Payload"].read().decode('utf-8')
