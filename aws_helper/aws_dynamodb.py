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
        return table.put_item(Item=item, ReturnValues='ALL_OLD', **kwargs)

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
        key1, val1 = key.popitem()
        key_exp = Key(key1).eq(val1)
        if key:
            key2, val2 = key.popitem()
            key_exp = key_exp + '&' + Key(key2).eq(val2)
        table = self.resource.Table(os.environ[table])
        response = table.query(KeyConditionExpression=key_exp, **kwargs)
        if "Items" in response and response["Items"]:
            return response["Items"]

    def update_item(self, table, key, updates=None, deletes=None, **kwargs):
        exp = ""
        counter = 1
        names = {}
        values = {}
        updates = updates or {}
        deletes = deletes or []
        updates = self.datetime_string(updates)
        updates["updated_on"] = datetime.datetime.utcnow().isoformat()
        if updates:
            for f in dict(updates):
                attr_placeholder = '#attr' + str(counter)
                val_placeholder = ':val' + str(counter)
                # replace key and val with placeholder
                updates[attr_placeholder] = val_placeholder
                # set placeholders in name and value
                names[attr_placeholder] = f
                values[val_placeholder] = updates[f]
                # delete original key and val
                del updates[f]

                counter += 1
            exp += 'SET '
            exp += ', '.join("{}={}".format(key, val) for (key, val) in updates.items())
            exp += ' '
        if deletes:
            for index, value in enumerate(deletes):
                val_placeholder = ':val' + str(counter)
                values[val_placeholder] = value
                deletes[index] = val_placeholder
                counter += 1
            exp += 'REMOVE '
            exp += ', '.join(deletes)
            exp += ' '
        table = self.resource.Table(os.environ[table])
        print(exp)
        return table.update_item(Key=key, ReturnValues='ALL_NEW', UpdateExpression=exp, ExpressionAttributeNames=names,
                                 ExpressionAttributeValues=values, **kwargs)
