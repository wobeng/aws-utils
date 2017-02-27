import json
from helper import misc
import os


class S3:
    def __init__(self, session):
        self._s3 = session.client("s3")

    def get_object(self, bucket, key, **kwargs):
        response = self._s3.get_object(Bucket=bucket, Key=key, **kwargs)
        response = response['Body'].read()
        return response

    def get_json_object(self, bucket, key, **kwargs):
        response = self.get_object(bucket, key, **kwargs)
        response = json.loads(response)
        return response

    def download_object(self, bucket, key, save_dir):
        output = os.path.join(save_dir, key.split("/")[-1])
        self._s3.meta.client.download_file(bucket, key, output)
        return output

    def cdn_find_and_replace(self,body,bucket,map):
        cdn_map = self.get_json_object(bucket,map)
        fnr = {}
        for path in cdn_map:
            find_path = path
            if find_path in body:
                fnr[find_path] = cdn_map[find_path]["fingerprint"]
        if fnr:
            replace = misc.make_xlat(fnr)
            body = replace(body)
        return body