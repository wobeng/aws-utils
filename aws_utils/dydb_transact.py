import datetime

from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

from aws_utils.dynamodb import DynamoDb


def decorate_get_item(item):
    if 'Item' in item and item['Item']:
        return deserialize_output(item['Item'])
    return {}


def serialize_input(value):
    output = {}
    for k, v in value.items():
        output[k] = TypeSerializer().serialize(v)
    return output


def deserialize_output(value):
    for k, v in dict(value).items():
        value[k] = TypeDeserializer().deserialize(v)
    return value


def decorate_input(kwargs):
    for k, v in dict(kwargs).items():
        if k in ['Key', 'ExpressionAttributeValues', 'Item']:
            kwargs[k] = serialize_input(v)
    return kwargs


class DynamoDbTransaction:
    def __init__(self, session):
        self.dynamodb = DynamoDb(session, dry_run=True)
        self.gets = []
        self.posts = []
        self.updates = []
        self.deletes = []
        self.condition_check = []

    def post_item(self, table, key, item, **kwargs):
        print(item)
        item.setdefault('created_on', datetime.datetime.utcnow().isoformat())
        _post_item = self.dynamodb.post_item(table, serialize_input(key), serialize_input(item), **kwargs)
        _output = {'Key': key, 'Table': table, 'Item': item}
        print(_post_item)
        self.posts.append((_post_item, _output))

    def update_item(self, table, key, updates=None, deletes=None, adds=None, appends=None, ensure_key_exist=True,
                    **kwargs):
        updates = updates or updates
        updates.setdefault('updated_on', datetime.datetime.utcnow().isoformat())
        _update_item = self.dynamodb.update_item(table, key, updates, deletes,
                                                 adds, appends, ensure_key_exist, **kwargs)
        _output = {'Key': key, 'Table': table, 'Updates': updates, 'Deletes': deletes,
                   'Adds': adds, 'Appends': appends}
        self.updates.append((_update_item, _output))

    def delete_item(self, table, key, **kwargs):
        _delete_item = self.dynamodb.delete_item(table, key, **kwargs)
        _output = {'Key': key, 'Table': table}
        self.deletes.append((_delete_item, _output))

    def condition_check(self, table, key, **kwargs):
        # use delete item dry run because parameters are the same
        _condition_check = self.dynamodb.delete_item(table, key, **kwargs)
        _output = {'Key': key, 'Table': table}
        self.condition_check.append((_condition_check, _output))

    def transact_write(self):
        transact_items = []
        m = {
            'Put': self.posts,
            'Update': self.updates,
            'Delete': self.deletes,
            'ConditionCheck': self.condition_check,
        }
        for k, v in m.items():
            if v:
                for item in v:
                    transact_items.append({k: item[0]})
        print(transact_items)
        response = self.dynamodb.client.transact_write_items(TransactItems=transact_items)
        print(response)

    def get_item(self, table, key, **kwargs):
        self.gets.append(self.dynamodb.get_item(table, serialize_input(key), **kwargs))
        return self

    def transact_read(self):
        transact_items = [{'Get': item} for item in self.gets]
        response = self.dynamodb.client.transact_get_items(TransactItems=transact_items)
        return [decorate_get_item(item) for item in response['Responses']]
