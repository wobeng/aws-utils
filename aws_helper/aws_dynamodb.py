import datetime

import os
from boto3.dynamodb.conditions import Key


class Dynamodb:
    def __init__(self, session):
        self.client = session.client("dynamodb")
        self.resource = session.resource("dynamodb")

    @staticmethod
    def datetime_string(item):
        for k in dict(item):
            if isinstance(item[k], datetime.datetime):
                item[k] = item[k].isoformat()
        return item

    def add_item(self, table, item, **kwargs):
        item = self.datetime_string(item)
        table = self.resource.Table(os.environ[table])
        return table.put_item(Item=item, ReturnValues='ALL_OLD', **kwargs)['Attributes']

    def post_item(self, table, item, **kwargs):
        item["created_on"] = datetime.datetime.utcnow().isoformat()
        return self.add_item(table, item=item, **kwargs)

    def put_item(self, table, item, **kwargs):
        item["updated_on"] = datetime.datetime.utcnow().isoformat()
        return self.add_item(table, item=item ** kwargs)

    def get_item(self, table, key, **kwargs):
        table = self.resource.Table(os.environ[table])
        response = table.get_item(Key=key, ConsistentRead=True, **kwargs)
        if "Item" in response and response["Item"]:
            return response["Item"]

    def delete_item(self, table, key, **kwargs):
        table = self.resource.Table(os.environ[table])
        return table.delete_item(Key=key, ReturnValues='ALL_OLD', **kwargs)

    def query(self, table, key, **kwargs):
        key_exp = ""
        key_exp += '& '.join(Key('%s').eq('%s') % (key, val) for (key, val) in list(key.items()))
        table = self.resource.Table(os.environ[table])
        response = table.query(KeyConditionExpression=key_exp, **kwargs)
        if "Items" in response and response["Items"]:
            return response["Items"]

    def update_item(self, table, key, updates=None, deletes=None, **kwargs):
        exp = ""
        counter = 1
        values = {}
        updates = updates or {}
        deletes = deletes or []
        updates = self.datetime_string(updates)
        updates["updated_on"] = datetime.datetime.utcnow().isoformat()
        if updates:
            for f in dict(updates):
                placeholder = ':val' + str(counter)
                values[placeholder] = updates[f]
                updates[f] = placeholder
                counter += 1
            exp += 'SET '
            exp += ', '.join("%s=%s" % (key, val) for (key, val) in list(updates.items()))
            exp += ' '
        if deletes:
            for index, value in enumerate(deletes):
                placeholder = ':val' + str(counter)
                values[placeholder] = value
                deletes[index] = placeholder
                counter += 1
            exp += 'REMOVE '
            exp += ', '.join(deletes)
            exp += ' '
        table = self.resource.Table(os.environ[table])
        return table.update_item(Key=key, ReturnValues='ALL_NEW', UpdateExpression=exp,
                                 ExpressionAttributeValues=values, **kwargs)
