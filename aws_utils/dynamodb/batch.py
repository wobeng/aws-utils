import random
import time

from aws_utils.dynamodb.utlis import deserialize_item, serialize_input, projection_string


class DynamoDbBatch:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.get_item_items = {}

    @projection_string
    def get_item(self, table, keys, **kwargs):
        kwargs['Keys'] = [serialize_input(k) for k in keys]
        self.get_item_items[table] = kwargs
        return self

    def batch_read(self):
        n = 0
        results = {}
        response = self.client.batch_get_item(RequestItems=self.get_item_items)
        results.update(response['Responses'])
        while response['UnprocessedKeys']:
            # Implement some kind of exponential back off here
            n = n + 1
            time.sleep((2 ** n) + random.randint(0, 1000) / 1000)
            response = self.client.batch_get_item(RequestItems=response['UnprocessedKeys'])
            results.update(response['Responses'])
        for table, records in dict(results).items():
            results[table] = [deserialize_item(r) for r in records]
        return results
