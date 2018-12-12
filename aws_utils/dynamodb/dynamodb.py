import random
import time

from boto3.dynamodb.conditions import Key

from aws_utils.dynamodb import base
from aws_utils.dynamodb.utlis import projection_string


class DynamoDb:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.resource = session.resource('dynamodb')
        self.get_items_queue = {}

    def __call__(self, table_name=None):
        if table_name:
            self.table_name = table_name
            self.table = self.resource.Table(table_name)
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

    @projection_string
    def add_get_items(self, keys, **kwargs):
        kwargs['Keys'] = keys
        self.get_items_queue[self.table] = kwargs
        return self

    @projection_string
    def query(self, partition_key, sort_key=None, **kwargs):
        key1, val1 = partition_key.popitem()
        key_exp = Key(key1).eq(val1)
        if sort_key:
            key_exp = key_exp & sort_key
        response = self.table.query(KeyConditionExpression=key_exp, **kwargs)
        if 'Items' in response and response['Items']:
            return {k: v for k, v in response.items() if k in ['Items', 'Count', 'ScannedCount', 'LastEvaluatedKey']}
        return {}

    def post_item(self, key, item, **kwargs):
        kwargs = base.post_item(key=key, item=item, **kwargs)
        kwargs['ReturnValues'] = 'ALL_OLD'
        response = self.table.put_item(**kwargs)
        response['Key'] = key
        response['Table'] = self.table_name
        response['Item'] = item
        return response

    def get_item(self, key, **kwargs):
        kwargs = base.get_item(key=key, **kwargs)
        response = self.table.get_item(**kwargs)
        if 'Item' in response and response['Item']:
            return response['Item']
        return {}

    def delete_item(self, key, **kwargs):
        kwargs = base.delete_item(key=key, **kwargs)
        kwargs['ReturnValues'] = 'ALL_OLD'
        response = self.table.delete_item(**kwargs)
        response['Key'] = key
        response['Table'] = self.table_name
        return response

    def update_item(self, key, updates=None, deletes=None, adds=None, appends=None, ensure_key_exist=True,
                    **kwargs):
        kwargs = base.update_item(
            key=key, updates=updates, deletes=deletes, adds=adds,
            appends=appends, ensure_key_exist=ensure_key_exist, **kwargs
        )
        kwargs['ReturnValues'] = 'ALL_OLD'
        response = self.table.update_item(**kwargs)
        response['Key'] = key
        response['Table'] = self.table_name
        response['Updates'] = updates
        response['Deletes'] = deletes
        response['Adds'] = adds
        response['Appends'] = appends
        return response
