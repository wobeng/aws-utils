import boto3
import os
from helper import misc

from aws_gateway import Gateway
from aws_lambda import Lambda
from aws_log import Log
from aws_s3 import S3


class Aws:
    def __init__(self, session=None, profile_name=None, region_name=None):

        # load instance if available
        try:
            import instance
            profile_name = instance.PROFILE
            region_name = instance.REGION
        except BaseException as e:
            pass

        if session:
            self.session = session
        else:
            self.session = boto3.session.Session(profile_name=profile_name, region_name=region_name)

        self.aws_gateway = Gateway(self.session)
        self.aws_lambda = Lambda(self.session)
        self.aws_log = Log(self.session)
        self.aws_s3 = S3(self.session)

    def load_config(self, bucket=None, key=None):

        # load config from db
        bucket = os.environ.get("CONFIG_BUCKET", bucket)
        key = os.environ.get("KEY", key)

        try:
            import instance
            bucket = instance.CONFIG_BUCKET
            key = instance.KEY
        except BaseException as e:
            pass

        config = self.aws_s3.get_json_object(bucket, key)
        misc.import_env_vars(config)
