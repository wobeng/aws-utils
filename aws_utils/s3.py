import json
import os
from collections import OrderedDict
from operator import itemgetter


class S3:
    def __init__(self, session):
        self.client = session.client('s3')

    def get_object(self, bucket, key, **kwargs):
        response = self.client.get_object(Bucket=bucket, Key=key, **kwargs)
        response = response['Body'].read().decode('utf-8')
        return response

    def get_json_object(self, bucket, key, sort=False, **kwargs):
        response = self.get_object(bucket, key, **kwargs)
        response = json.loads(response)
        if sort:
            response = OrderedDict(sorted(response.items(), key=itemgetter(1)))
        return response

    def download_object(self, bucket, key, save_dir):
        output = os.path.join(save_dir, key.split('/')[-1])
        self.client.download_file(bucket, key, output)
        return output

    def generate_sign(self, bucket, key, size, conditions=None, secure=False, content_type_prefix=None):
        if not conditions:
            conditions = list()
        if secure:
            conditions.append({'x-amz-server-side-encryption': 'AES256'})
        if content_type_prefix:
            conditions.append(['starts-with', '$Content-Type', content_type_prefix + '/'])
        conditions.append(['content-length-range', 1, size])
        conditions.append({'success_action_status': '201'})
        return self.client.generate_presigned_post(
            bucket,
            key,
            Fields=None,
            Conditions=conditions,
            ExpiresIn=3600
        )
