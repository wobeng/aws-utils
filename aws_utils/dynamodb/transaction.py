from aws_utils.dynamodb import base
from aws_utils.dynamodb.utlis import deserialize_item, transaction


class DynamoDbTransaction:
    def __init__(self, session):
        self.client = session.client('dynamodb')
        self.get_item_items = []
        self.post_item_items = []
        self.update_item_items = []
        self.delete_item_items = []
        self.condition_check_items = []

    def __call__(self, table_name=None):
        if table_name:
            self.table_name = table_name
        return self

    @transaction
    def post_item(self, key, item, **kwargs):
        return base.post_item(key=key, item=item, **kwargs)

    @transaction
    def update_item(self, key, updates=None, deletes=None, adds=None, appends=None, ensure_key_exist=True,
                    **kwargs):
        return base.update_item(
            key=key, updates=updates, deletes=deletes,
            adds=adds, appends=appends, ensure_key_exist=ensure_key_exist, **kwargs
        )

    @transaction
    def delete_item(self, key, **kwargs):
        return base.delete_item(key=key, **kwargs)

    @transaction
    def condition_check(self, key, **kwargs):
        return base.delete_item(key=key, **kwargs)  # use delete because its the same structure

    @transaction
    def get_item(self, key, **kwargs):
        return base.get_item(key=key, **kwargs)

    def transact_write(self):
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
        response = self.client.transact_write_items(TransactItems=transact_items)
        return response

    def transact_read(self):
        transact_items = [{'Get': item} for item in self.get_item_items]
        response = self.client.transact_get_items(TransactItems=transact_items)
        return [deserialize_item(item) for item in response['Responses'] if item]
