from boto3.dynamodb.conditions import Attr

from aws_utils import datetime_utc
from aws_utils.dynamodb.utlis import convert_types, projection_string, random_id


@convert_types
@projection_string
def post_item(key, item, ensure_key_not_exist=True, **kwargs):
    item = dict(item) or {}
    item.update(key)
    item.setdefault('created_on', datetime_utc().isoformat())

    # ensure not key exist or reject
    if ensure_key_not_exist:
        key_not_exist_conditions = None
        for k, v in key.items():
            if key_not_exist_conditions:
                key_not_exist_conditions = key_not_exist_conditions and Attr(k).ne(v)
            else:
                key_not_exist_conditions = Attr(k).ne(v)

        if 'ConditionExpression' in kwargs:
            kwargs['ConditionExpression'] = kwargs['ConditionExpression'] & key_not_exist_conditions
        else:
            kwargs['ConditionExpression'] = key_not_exist_conditions

    kwargs['Item'] = item
    return kwargs


@projection_string
def get_item(key, **kwargs):
    kwargs['Key'] = key
    return kwargs


def delete_item(key, **kwargs):
    kwargs['Key'] = key
    return kwargs


@convert_types
@projection_string
def update_item(key, updates=None, deletes=None, adds=None, appends=None, ensure_key_exist=True,
                **kwargs):
    exp = ''
    names = {}
    values = {}
    updates = dict(updates or {})
    deletes = list(deletes or [])
    adds = dict(adds or {})
    appends = dict(appends or {})
    updates.setdefault('updated_on', datetime_utc().isoformat())

    def add_attribute(attribute):
        if '.' not in attribute:
            element = ''
            if '[' in attribute and ']' in attribute:
                element = attribute[-3:]
                attribute = attribute[:-3]
            attr_placeholder = '#attr' + random_id()
            names[attr_placeholder] = attribute
            return attr_placeholder + element
        attributes = attribute.split('.')
        for _idx, _val in enumerate(attributes):
            element = ''
            if '[' in _val and ']' in _val:
                element = _val[-3:]
                _val = _val[:-3]
            attr_placeholder = '#attr' + random_id()
            attributes[_idx] = attr_placeholder + element
            names[attr_placeholder] = _val
        return '.'.join(attributes)

    def add_value(value):
        val_placeholder = ':val' + random_id()
        values[val_placeholder] = value
        return val_placeholder

    if appends or updates:
        exp += 'SET '
    if appends:
        for k1, v1 in dict(appends).items():
            appends[add_attribute(k1)] = add_value(v1)
            del appends[k1]
        exp += ', '.join('{0}=list_append({0},{1})'.format(k2, v2) for (k2, v2) in appends.items())
    if updates:
        for k1, v1 in dict(updates).items():
            updates[add_attribute(k1)] = add_value(v1)
            del updates[k1]
        if exp != 'SET ':
            exp += ', '
        exp += ', '.join('{}={}'.format(k2, v2) for (k2, v2) in updates.items())
    if appends or updates:
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

    # ensure key exist or reject
    if ensure_key_exist:
        key_exist_conditions = None
        for k, v in key.items():
            if key_exist_conditions:
                key_exist_conditions and Attr(k).eq(v)
            else:
                key_exist_conditions = Attr(k).eq(v)

        if 'ConditionExpression' in kwargs:
            kwargs['ConditionExpression'] = kwargs['ConditionExpression'] & key_exist_conditions
        else:
            kwargs['ConditionExpression'] = key_exist_conditions

    kwargs['Key'] = key
    kwargs['UpdateExpression'] = exp
    kwargs['ExpressionAttributeNames'] = names
    kwargs['ExpressionAttributeValues'] = values
    return kwargs
