import copy
import datetime
import random
import time
import uuid
from decimal import Decimal

from boto3.dynamodb.conditions import Attr, Key


class DynamoDb:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.resource = session.resource('dynamodb')
        self.get_items_queue = {}

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

    @staticmethod
    def random_id():
        return str(uuid.uuid4()).split('-')[0]

    def post_item(self, table, key, item, **kwargs):
        _item = copy.deepcopy(item) or {}
        _item['created_on'] = datetime.datetime.utcnow().isoformat()
        _item.update(key)
        _item = DynamoDb.convert_types(_item)
        _table = self.resource.Table(table)
        response = _table.put_item(Item=_item, ReturnValues='ALL_OLD', **kwargs)
        response['Key'] = key
        response['Table'] = table
        response['Item'] = item
        return response

    def get_item(self, table, key, **kwargs):
        kwargs = DynamoDb.projection_string(kwargs)
        _table = self.resource.Table(table)
        response = _table.get_item(Key=key, **kwargs)
        if 'Item' in response and response['Item']:
            return response['Item']
        return {}

    def add_get_items(self, table, keys, **kwargs):
        kwargs['Keys'] = keys
        kwargs = DynamoDb.projection_string(kwargs)
        self.get_items_queue[table] = kwargs
        return self

    def get_items(self):
        n = 0
        results = {}
        response = self.client.batch_get_item(RequestItems=self.get_items_queue)
        results.update(response['Responses'])
        while response['UnprocessedKeys']:
            # Implement some kind of exponential back off here
            n = n + 1
            time.sleep((2 ** n) + random.randint(0, 1000) / 1000)
            response = self.client.batch_get_item(RequestItems=response['UnprocessedKeys'])
            results.update(response['Responses'])
        return results

    def delete_item(self, table, key, **kwargs):
        _table = self.resource.Table(table)
        response = _table.delete_item(Key=key, ReturnValues='ALL_OLD', **kwargs)
        response['Key'] = key
        response['Table'] = table
        return response

    def query(self, table, partition_key, sort_key=None, **kwargs):
        kwargs = DynamoDb.projection_string(kwargs)
        key1, val1 = partition_key.popitem()
        key_exp = Key(key1).eq(val1)
        if sort_key:
            key_exp = key_exp & sort_key
        _table = self.resource.Table(table)
        response = _table.query(KeyConditionExpression=key_exp, **kwargs)
        if 'Items' in response and response['Items']:
            return {k: v for k, v in response.items() if k in ['Items', 'Count', 'ScannedCount', 'LastEvaluatedKey']}
        return {}

    def update_item(self, table, key, updates=None, deletes=None, adds=None, appends=None, ensure_key_exist=True,
                    **kwargs):
        exp = ''
        names = {}
        values = {}
        _updates = copy.deepcopy(updates) or {}
        _deletes = copy.deepcopy(deletes) or []
        _adds = copy.deepcopy(adds) or {}
        _appends = copy.deepcopy(appends) or {}
        _updates = DynamoDb.convert_types(_updates)
        _updates['updated_on'] = datetime.datetime.utcnow().isoformat()

        def add_attribute(attribute):
            if '.' not in attribute:
                attr_placeholder = '#attr' + self.random_id()
                names[attr_placeholder] = attribute
                return attr_placeholder
            attributes = attribute.split('.')
            for _idx, _val in enumerate(attributes):
                attr_placeholder = '#attr' + self.random_id()
                attributes[_idx] = attr_placeholder
                names[attr_placeholder] = _val
            return '.'.join(attributes)

        def add_value(value):
            val_placeholder = ':val' + self.random_id()
            values[val_placeholder] = value
            return val_placeholder

        if _appends:
            for k1, v1 in dict(_appends).items():
                _appends[add_attribute(k1)] = add_value(v1)
                del _appends[k1]
            exp += 'SET '
            exp += ', '.join('{0}=list_append({0},{1})'.format(k2, v2) for (k2, v2) in _appends.items())
            exp += ' '
        if _updates:
            for k1, v1 in dict(_updates).items():
                _updates[add_attribute(k1)] = add_value(v1)
                del _updates[k1]
            exp += 'SET '
            exp += ', '.join('{}={}'.format(k2, v2) for (k2, v2) in _updates.items())
            exp += ' '
        if _deletes:
            for k3, v3 in enumerate(_deletes):
                _deletes[k3] = add_attribute(v3)
            exp += 'REMOVE '
            exp += ', '.join(_deletes)
            exp += ' '
        if _adds:
            for k4, v4 in dict(_adds).items():
                _adds[add_attribute(k4)] = add_value(v4)
                del _adds[k4]
            exp += 'ADD '
            exp += ', '.join('{} {}'.format(k5, v5) for (k5, v5) in _adds.items())
            exp += ' '
        _table = self.resource.Table(table)

        # ensure key exist or reject
        if ensure_key_exist:
            key_exist_conditions = None
            for k, v in key.items():
                key_exist_conditions = key_exist_conditions & Attr(k).eq(v) if key_exist_conditions else Attr(k).eq(v)

            if 'ConditionExpression' in kwargs:
                kwargs['ConditionExpression'] = kwargs['ConditionExpression'] & key_exist_conditions
            else:
                kwargs['ConditionExpression'] = key_exist_conditions

        response = _table.update_item(
            Key=key, UpdateExpression=exp,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values, **kwargs,
            ReturnValues='ALL_OLD'
        )
        response['Key'] = key
        response['Table'] = table
        response['Updates'] = updates
        response['Deletes'] = deletes
        response['Adds'] = adds
        response['Appends'] = appends
        return response
