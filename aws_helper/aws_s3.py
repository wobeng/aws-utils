import json
from collections import OrderedDict
from operator import itemgetter

import os
from helper import misc


class S3:
    def __init__(self, session):
        self.client = session.client("s3")

    def get_object(self, bucket, key, **kwargs):
        response = self.client.get_object(Bucket=bucket, Key=key, **kwargs)
        response = response['Body'].read()
        return response

    def get_json_object(self, bucket, key, sort=False, **kwargs):
        response = self.get_object(bucket, key, **kwargs)
        response = json.loads(response)
        if sort:
            response = OrderedDict(sorted(response.items(), key=itemgetter(1)))
        return response

    def download_object(self, bucket, key, save_dir):
        output = os.path.join(save_dir, key.split("/")[-1])
        self.client.download_file(bucket, key, output)
        return output

    def generate_sign(self, bucket, key, size, secure=False, content_type_prefix = None):
        conditions = list()
        conditions.append(["content-length-range", 1, size])
        conditions.append({"success_action_status": "201"})
        if secure:
            conditions.append({"x-amz-server-side-encryption", "AES256"})
        if content_type_prefix:
            conditions.append(["starts-with", "$Content-Type", content_type_prefix + "/"])
        return self.client.generate_presigned_post(
            bucket,
            key,
            Fields=None,
            Conditions=conditions,
            ExpiresIn=3600
        )

    def cdn_find_and_replace(self, body, bucket, map):
        cdn_map = self.get_json_object(bucket, map)
        fnr = {}
        for path in cdn_map:
            find_path = path
            if find_path in body:
                fnr[find_path] = cdn_map[find_path]["fingerprint"]
        if fnr:
            replace = misc.make_xlat(fnr)
            body = replace(body)
        return body
