import datetime
import os
import uuid
from decimal import Decimal

from boto3.dynamodb.conditions import Key


class DynamoDb:
    def __init__(self, session):
        self.client = session.client("dynamodb")
        self.resource = session.resource("dynamodb")

    @staticmethod
    def convert_types(item):
        for k in dict(item):
            if isinstance(item[k], datetime.datetime):
                item[k] = item[k].isoformat()
            elif isinstance(item[k], float):
                item[k] = Decimal(str(item[k]))
            elif isinstance(item[k], dict):
                item[k] = DynamoDb.convert_types(item[k])
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

    def post_item(self, table, key, item, **kwargs):
        item["created_on"] = datetime.datetime.utcnow().isoformat()
        item.update(key)
        item = DynamoDb.convert_types(item)
        table = self.resource.Table(os.environ[table])
        response = table.put_item(Item=item, ReturnValues='ALL_OLD', **kwargs)
        response['Key'] = key
        return response

    def get_item(self, table, key, **kwargs):
        kwargs = DynamoDb.projection_string(kwargs)
        table = self.resource.Table(os.environ[table])
        response = table.get_item(Key=key, **kwargs)
        if "Item" in response and response["Item"]:
            return response["Item"]

    def delete_item(self, table, key, **kwargs):
        table = self.resource.Table(os.environ[table])
        response = table.delete_item(Key=key, ReturnValues='ALL_OLD', **kwargs)
        response['Key'] = key
        return response

    def query(self, table, partition_key, sort_key=None, **kwargs):
        kwargs = DynamoDb.projection_string(kwargs)
        key1, val1 = partition_key.popitem()
        key_exp = Key(key1).eq(val1)
        if sort_key:
            key_exp = key_exp & sort_key
        table = self.resource.Table(os.environ[table])
        response = table.query(KeyConditionExpression=key_exp, **kwargs)
        if "Items" in response and response["Items"]:
            return response["Items"]

    def update_item(self, table, key, updates=None, deletes=None, **kwargs):
        exp = ""
        names = {}
        values = {}
        updates = updates or {}
        deletes = deletes or []
        updates = DynamoDb.convert_types(updates)
        updates["updated_on"] = datetime.datetime.utcnow().isoformat()

        def random_id():
            return str(uuid.uuid4()).split('-')[0]

        def add_attribute(a):
            if '.' in a:
                return _add_nested_attribute(a)
            return _add_attribute(a)

        def add_value(v):
            val_placeholder = ':val' + random_id()
            values[val_placeholder] = v
            return val_placeholder

        def _add_attribute(a):
            attr_placeholder = '#attr' + random_id()
            names[attr_placeholder] = a
            return attr_placeholder

        def _add_nested_attribute(a):
            attributes = a.split('.')
            for _idx, _val in enumerate(attributes):
                attr_placeholder = '#attr' + random_id()
                attributes[_idx] = attr_placeholder
                names[attr_placeholder] = _val
            return '.'.join(attributes)

        if updates:
            for k, v in dict(updates).items():
                updates[add_attribute(k)] = add_value(v)
                del updates[k]
            exp += 'SET '
            exp += ', '.join("{}={}".format(k, v) for (k, v) in updates.items())
            exp += ' '
        if deletes:
            for index, value in enumerate(deletes):
                deletes[index] = add_attribute(value)
            exp += 'REMOVE '
            exp += ', '.join(deletes)
            exp += ' '
        table = self.resource.Table(os.environ[table])
        response = table.update_item(Key=key, UpdateExpression=exp, ExpressionAttributeNames=names,
                                     ExpressionAttributeValues=values, **kwargs)
        response['Key'] = key
        return response
