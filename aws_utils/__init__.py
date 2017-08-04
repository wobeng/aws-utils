# Copyright 2015-2016 Welby Obeng.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__title__ = 'aws utils'
__version__ = '1.0.0'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright Welby Obeng 2017 - present'
__url__ = 'https://github.com/wobeng/aws-utils'

import boto3
import os
from py_utils import misc

from aws_utils.cognito import Cognito
from aws_utils.dynamodb import DynamoDb
from aws_utils.gateway import Gateway
from aws_utils.alambda import Lambda
from aws_utils.cloudwatch import CloudWatch
from aws_utils.s3 import S3


class Aws:
    def __init__(self, session=None, profile_name=None, region_name=None):

        # load instance if available
        try:
            import instance
            profile_name = instance.PROFILE
            region_name = instance.REGION
        except BaseException:
            pass

        if session:
            self.session = session
        else:
            self.session = boto3.session.Session(profile_name=profile_name, region_name=region_name)

        self.aws_gateway = Gateway(self.session)
        self.aws_lambda = Lambda(self.session)
        self.aws_log = CloudWatch(self.session)
        self.aws_s3 = S3(self.session)
        self.aws_dynamodb = DynamoDb(self.session)
        self.aws_cognito = Cognito(self.session)

    def load_config(self, bucket=None, key=None):

        # load config from db
        bucket = os.environ.get("CONFIG_BUCKET", bucket)
        key = os.environ.get("KEY", key)

        try:
            import instance
            bucket = instance.CONFIG_BUCKET
            key = instance.KEY
        except BaseException:
            pass

        config = self.aws_s3.get_json_object(bucket, key)
        misc.import_env_vars(config)


def client(session=None, profile_name=None, region_name=None):
    aws = Aws(session,profile_name,region_name)
    if os.environ.get('SERVERTYPE', "DEV") == "DEV":
        aws.load_config()
    return aws
