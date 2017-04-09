import os

class Dynamodb:
    def __init__(self, session):
        self.client = session.client("dynamodb")
        self.resource = session.resource("dynamodb")

    def put_item(self, table, item):
        table = self.resource.Table(os.environ[table])
        table.put_item(Item=item)

    def get_item(self, table, key):
        table = self.resource.Table(os.environ[table])
        response = table.get_item(Key=key, ConsistentRead=True)
        if "Item" in response and response["Item"]:
            return response["Item"]

    def query(self,table,attributes):
        table = self.resource.Table(os.environ[table])
        response = table.query(**attributes)
        if ["Items"] in response and response["Items"]:
            return response["Items"]
