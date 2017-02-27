import json


class Lambda:
    def __init__(self, session):
        self._lambda = session.client("lambda")

    def invoke(self, function_name, payload):
        response = self._lambda.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        if response["StatusCode"] != 200 or "FunctionError" in response:
            response["Payload"] = response["Payload"].read()
            raise BaseException(response)
        return json.loads(response["Payload"].read())
