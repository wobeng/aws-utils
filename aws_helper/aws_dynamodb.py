import datetime

import os


class Dynamodb:
    def __init__(self, session):
        self.client = session.client("dynamodb")
        self.resource = session.resource("dynamodb")

    def add_item(self, table, **kwargs):
        table = self.resource.Table(os.environ[table])
        table.put_item(**kwargs)

    def post_item(self, table, **kwargs):
        if "Item" in kwargs:
            kwargs["Item"]["created_on"] = datetime.datetime.utcnow().isoformat()
        self.add_item(table, **kwargs)

    def put_item(self, table, **kwargs):
        if "Item" in kwargs:
            kwargs["Item"]["updated_on"] = datetime.datetime.utcnow().isoformat()
        self.add_item(table, **kwargs)

    def get_item(self, table, **kwargs):
        table = self.resource.Table(os.environ[table])
        response = table.get_item(ConsistentRead=True, **kwargs)
        if "Item" in response and response["Item"]:
            return response["Item"]

    def query(self, table, **kwargs):
        table = self.resource.Table(os.environ[table])
        response = table.query(**kwargs)
        if "Items" in response and response["Items"]:
            return response["Items"]

    def delete_item(self, table, **kwargs):
        table = self.resource.Table(os.environ[table])
        table.delete_item(**kwargs)
