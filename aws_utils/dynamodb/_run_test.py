from aws_utils import client

aws = client()

dydb = aws.dydb
dydb = dydb(table_name='CaseFeed')

output = dydb.get_item(
    key={'case_id': 'case_id-post', 'post_id': 'post_id-post'}
)
output = dydb.update_item(
    key={'case_id': 'case_id-post', 'post_id': 'post_id-post'},
    updates={'info2': 'info234'}
)
print(output)
