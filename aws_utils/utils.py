import datetime
from decimal import Decimal


def convert_types(item):
    for k in dict(item):
        if isinstance(item[k], datetime.datetime):
            item[k] = item[k].isoformat()
        elif isinstance(item[k], float):
            item[k] = Decimal(str(item[k]))
        elif isinstance(item[k], dict):
            item[k] = convert_types(item[k])
    return item


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
