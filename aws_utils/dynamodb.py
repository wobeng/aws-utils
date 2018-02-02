import datetime
import uuid
from decimal import Decimal

from boto3.dynamodb.conditions import Attr, Key


class DynamoDb:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.resource = session.resource('dynamodb')

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
        item['created_on'] = datetime.datetime.utcnow().isoformat()
        item.update(key)
        item = DynamoDb.convert_types(item)
        table = self.resource.Table(table)
        response = table.put_item(Item=item, ReturnValues='ALL_OLD', **kwargs)
        response['Key'] = key
        return response

    def get_item(self, table, key, **kwargs):
        kwargs = DynamoDb.projection_string(kwargs)
        table = self.resource.Table(table)
        response = table.get_item(Key=key, **kwargs)
        if 'Item' in response and response['Item']:
            return response['Item']
        return {}

    def delete_item(self, table, key, **kwargs):
        table = self.resource.Table(table)
        response = table.delete_item(Key=key, ReturnValues='ALL_OLD', **kwargs)
        response['Key'] = key
        return response

    def query(self, table, partition_key, sort_key=None, **kwargs):
        kwargs = DynamoDb.projection_string(kwargs)
        key1, val1 = partition_key.popitem()
        key_exp = Key(key1).eq(val1)
        if sort_key:
            key_exp = key_exp & sort_key
        table = self.resource.Table(table)
        response = table.query(KeyConditionExpression=key_exp, **kwargs)
        if 'Items' in response and response['Items']:
            return {k: v for k, v in response.items() if k in ['Items', 'Count', 'ScannedCount', 'LastEvaluatedKey']}
        return {}

    def update_item(self, table, key, updates=None, deletes=None, adds=None, appends=None, **kwargs):
        exp = ''
        names = {}
        values = {}
        updates = updates or {}
        deletes = deletes or []
        updates = DynamoDb.convert_types(updates)
        updates['updated_on'] = datetime.datetime.utcnow().isoformat()

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

        if appends:
            for k1, v1 in dict(appends).items():
                appends[add_attribute(k1)] = add_value(v1)
                del appends[k1]
            exp += 'SET '
            exp += ', '.join('{0}=list_append({0},{1})'.format(k2, v2) for (k2, v2) in appends.items())
            exp += ' '
        if updates:
            for k1, v1 in dict(updates).items():
                updates[add_attribute(k1)] = add_value(v1)
                del updates[k1]
            exp += 'SET '
            exp += ', '.join('{}={}'.format(k2, v2) for (k2, v2) in updates.items())
            exp += ' '
        if deletes:
            for k3, v3 in enumerate(deletes):
                deletes[k3] = add_attribute(v3)
            exp += 'REMOVE '
            exp += ', '.join(deletes)
            exp += ' '
        if adds:
            for k4, v4 in dict(adds).items():
                adds[add_attribute(k4)] = add_value(v4)
                del adds[k4]
            exp += 'ADD '
            exp += ', '.join('{} {}'.format(k5, v5) for (k5, v5) in adds.items())
            exp += ' '
        table = self.resource.Table(table)

        # ensure key exist or reject
        key_exist_conditions = None
        for k, v in key.items():
            key_exist_conditions = key_exist_conditions & Attr(k).eq(v) if key_exist_conditions else Attr(k).eq(v)

        if 'ConditionExpression' in kwargs:
            kwargs['ConditionExpression'] = kwargs['ConditionExpression'] & key_exist_conditions
        else:
            kwargs['ConditionExpression'] = key_exist_conditions

        response = table.update_item(
            Key=key, UpdateExpression=exp,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values, **kwargs
        )
        response['Key'] = key
        return response
