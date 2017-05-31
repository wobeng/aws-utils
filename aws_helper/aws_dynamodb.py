import datetime
from decimal import Decimal

import os
from boto3.dynamodb.conditions import Key


class DynamoDb:
    def __init__(self, session):
        self.client = session.client("dynamodb")
        self.resource = session.resource("dynamodb")

    def convert_types(self, item):
        for k in dict(item):
            if isinstance(item[k], datetime.datetime):
                item[k] = item[k].isoformat()
            elif isinstance(item[k], float):
                item[k] = Decimal(str(item[k]))
            elif isinstance(item[k], dict):
                item[k] = self.convert_types(item[k])
        return item

    @staticmethod
    def projection_string(kwargs):
        if 'ProjectionExpression' in kwargs:
            names = {}
            counter = 1
            attributes = kwargs['ProjectionExpression'].split(',')
            for a_index, attribute in enumerate(attributes):
                sub_attributes = attribute.split('.')
                for sa_index, sub_attribute in enumerate(sub_attributes):
                    place_holder = '#attr' + str(counter)
                    names[place_holder] = sub_attribute
                    sub_attributes[sa_index] = place_holder
                    counter += 1
                attribute = '.'.join(sub_attributes)
                attributes[a_index] = attribute
            kwargs['ProjectionExpression'] = ','.join(attributes)
            kwargs['ExpressionAttributeNames'] = names
        return kwargs

    def add_item(self, table, key, item, **kwargs):
        item.update(key)
        item = self.convert_types(item)
        table = self.resource.Table(os.environ[table])
        table.put_item(Item=item, **kwargs)
        return key

    def post_item(self, table, key, item, **kwargs):
        item["created_on"] = datetime.datetime.utcnow().isoformat()
        return self.add_item(table, key, item=item, **kwargs)

    def put_item(self, table, key, item, **kwargs):
        item["updated_on"] = datetime.datetime.utcnow().isoformat()
        return self.add_item(table, key, item=item ** kwargs)

    def get_item(self, table, key, **kwargs):
        kwargs = self.projection_string(kwargs)
        table = self.resource.Table(os.environ[table])
        response = table.get_item(Key=key, **kwargs)
        if "Item" in response and response["Item"]:
            return response["Item"]

    def delete_item(self, table, key, **kwargs):
        table = self.resource.Table(os.environ[table])
        table.delete_item(Key=key, **kwargs)
        return key

    def query(self, table, key, **kwargs):
        kwargs = self.projection_string(kwargs)
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
        updates = self.convert_types(updates)
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
                attr_placeholder = '#attr' + str(counter)
                names[attr_placeholder] = value
                deletes[index] = attr_placeholder
                counter += 1
            exp += 'REMOVE '
            exp += ', '.join(deletes)
            exp += ' '
        table = self.resource.Table(os.environ[table])
        table.update_item(Key=key, UpdateExpression=exp, ExpressionAttributeNames=names,
                          ExpressionAttributeValues=values, **kwargs)
        return key
