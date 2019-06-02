from aws_utils.dynamodb import base
from aws_utils.dynamodb.utlis import deserialize_item, queue_input


class DynamoDbTransaction:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.get_item_items = []
        self.post_item_items = []
        self.update_item_items = []
        self.delete_item_items = []
        self.condition_check_items = []

    @queue_input
    def post_item(self, table, key, item, **kwargs):
        return base.post_item(TableName=table, key=key, item=item, **kwargs)

    @queue_input
    def update_item(self, table, key, updates=None, deletes=None, adds=None, appends=None, ensure_key_exist=True,
                    **kwargs):
        return base.update_item(
            TableName=table, key=key, updates=updates, deletes=deletes,
            adds=adds, appends=appends, ensure_key_exist=ensure_key_exist, **kwargs
        )

    @queue_input
    def delete_item(self, table, key, **kwargs):
        return base.delete_item(TableName=table, key=key, **kwargs)

    @queue_input
    def condition_check(self, table, key, **kwargs):
        return base.delete_item(TableName=table, key=key, **kwargs)  # use delete because its the same structure

    @queue_input
    def get_item(self, table, key, **kwargs):
        return base.get_item(TableName=table, key=key, **kwargs)

    def transact_write(self, debug=False):
        transact_items = []
        m = {
            'Put': self.post_item_items,
            'Update': self.update_item_items,
            'Delete': self.delete_item_items,
            'ConditionCheck': self.condition_check_items,
        }
        for k, v in m.items():
            if v:
                for item in v:
                    transact_items.append({k: item})
        if debug:
            print(transact_items)
        response = self.client.transact_write_items(TransactItems=transact_items)
        return response

    def transact_read(self, debug=False):
        transact_items = [{'Get': item} for item in self.get_item_items]
        if debug:
            print(transact_items)
        response = self.client.transact_get_items(TransactItems=transact_items)
        return [deserialize_item(item) for item in response['Responses'] if item]
