import random
import time

from aws_utils.dynamodb import base
from aws_utils.dynamodb.utlis import deserialize_item, queue_input


class DynamoDbBatch:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.get_item_items = []

    @queue_input
    def get_item(self, table, key, **kwargs):
        return base.get_item(TableName=table, key=key, **kwargs)

    def batch_read(self):
        n = 0
        results = {}
        request_items = {}
        print(self.get_item_items)
        for k in self.get_item_items:
            request_items[k.pop('TableName')] = k
        response = self.client.batch_get_item(RequestItems=request_items)
        results.update(response['Responses'])
        while response['UnprocessedKeys']:
            # Implement some kind of exponential back off here
            n = n + 1
            time.sleep((2 ** n) + random.randint(0, 1000) / 1000)
            response = self.client.batch_get_item(RequestItems=response['UnprocessedKeys'])
            results.update(response['Responses'])
        return {k: deserialize_item(v) for k, v in results.items()}
