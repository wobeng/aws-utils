from aws_utils import client

aws = client()

dydb_transact = aws.dydb_transact

dydb_transact.post_item(
    table='CaseFeed',
    key={
        'case_id': 'case_id-post',
        'post_id': 'post_id-post'
    },
    item={'info': 'info'}
)
dydb_transact.update_item(
    table='CaseFeed',
    key={
        'case_id': 'case_id1',
        'post_id': 'post_id1'
    },
    updates={'info-update': 'info-update'}
)
print(dydb_transact.transact_write())
