from aws_utils import client

aws = client()

dydb_transact = aws.dydb_transact
dydb_transact = dydb_transact(table_name='CaseFeed')

"""
dydb_transact.get_item(
    key={
        'case_id': 'case_id-post',
        'post_id': 'post_id-post'
    },
    ProjectionExpression='info'
)
dydb_transact.transact_read()
"""
dydb_transact.update_item(
    key={
        'case_id': 'case_id-post',
        'post_id': 'post_id-post'
    },
    updates={'info2' : 'info2'}
)

dydb_transact.transact_write()
