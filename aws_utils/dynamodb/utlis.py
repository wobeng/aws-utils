import datetime
import uuid
from decimal import Decimal

from boto3.dynamodb.conditions import ConditionExpressionBuilder
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer


def transaction(func):
    def wrapper(*args, **kwargs):
        kwargs = func(*args, **kwargs)
        self = args[0]
        if kwargs.get('Key', False):
            kwargs['Key'] = serialize_input(kwargs['Key'])
        if kwargs.get('Item', False):
            kwargs['Item'] = serialize_input(kwargs['Item'])
        if kwargs.get('ExpressionAttributeValues', False):
            kwargs['ExpressionAttributeValues'] = serialize_input(kwargs['ExpressionAttributeValues'])
        if kwargs.get('ConditionExpression', False):
            exp_string, names, values = ConditionExpressionBuilder().build_expression(kwargs['ConditionExpression'])
            values = serialize_input(values)
            kwargs['ConditionExpression'] = exp_string
            if 'ExpressionAttributeNames' in kwargs:
                kwargs['ExpressionAttributeNames'].update(names)
            else:
                kwargs['ExpressionAttributeNames'] = names
            if 'ExpressionAttributeValues' in kwargs:
                kwargs['ExpressionAttributeValues'].update(values)
            else:
                kwargs['ExpressionAttributeValues'] = values
        getattr(self, func.__name__ + '_items').append(kwargs)
        return self

    return wrapper


def convert_types(func):
    def main(item):
        for k in dict(item):
            if isinstance(item[k], datetime.datetime):
                item[k] = item[k].isoformat()
            elif isinstance(item[k], float):
                item[k] = Decimal(str(item[k]))
            elif isinstance(item[k], dict):
                item[k] = main(item[k])
        return item

    def wrapper(*args, **kwargs):
        args = list(args)
        if kwargs.get('item', False):
            kwargs['item'] = main(kwargs['item'])
        if kwargs.get('updates', False):
            kwargs['updates'] = main(kwargs['updates'])
        return func(*args, **kwargs)

    return wrapper


def projection_string(func):
    def wrapper(*args, **kwargs):
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
        return func(*args, **kwargs)

    return wrapper


def random_id():
    return str(uuid.uuid4()).split('-')[0]


def deserialize_item(item):
    if item.get('Item', False):
        return deserialize_output(item['Item'])
    return {}


def serialize_input(value):
    output = {}
    ty = TypeSerializer()
    for k, v in value.items():
        output[k] = ty.serialize(v)
    return output


def deserialize_output(value):
    ty = TypeDeserializer()
    for k, v in dict(value).items():
        value[k] = ty.deserialize(v)
    return value


def decorate_input(kwargs):
    for k, v in dict(kwargs).items():
        if k in ['Key', 'ExpressionAttributeValues', 'Item']:
            kwargs[k] = serialize_input(v)
    return kwargs
