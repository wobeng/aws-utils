import random
import time

from aws_utils.dynamodb.utlis import deserialize_output, serialize_input, projection_string


class DynamoDbBatch:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.request_items = {}

    @projection_string
    def get_item(self, table, keys, **kwargs):
        kwargs['Keys'] = [serialize_input(k) for k in keys]
        self.request_items[table] = kwargs
        return self

    def post_item(self, table, item):
        if table not in self.request_items:
            self.request_items[table] = []
        self.request_items[table].append({'PutRequest': {'Item':  serialize_input(item)}})


    def delete_item(self, table, key):
        if table not in self.request_items:
            self.request_items[table] = []
        self.request_items[table].append({'DeleteRequest': {'Key':  serialize_input(key)}})

    def batch_read(self):
        n = 0
        results = {}
        response = self.client.batch_get_item(RequestItems=self.request_items)
        results.update(response['Responses'])
        while response['UnprocessedKeys']:
            # Implement some kind of exponential back off here
            n = n + 1
            time.sleep((2 ** n) + random.randint(0, 1000) / 1000)
            response = self.client.batch_get_item(RequestItems=response['UnprocessedKeys'])
            results.update(response['Responses'])
        for table, records in dict(results).items():
            results[table] = [deserialize_output(r) for r in records]
        return results


    def batch_write(self):
        n = 0
        response = self.client.batch_write_item(RequestItems=self.request_items)
        while response['UnprocessedItems']:
            # Implement some kind of exponential back off here
            n = n + 1
            time.sleep((2 ** n) + random.randint(0, 1000) / 1000)
            response = self.client.batch_write_item(RequestItems=response['UnprocessedItems'])

