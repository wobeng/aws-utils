import json
import logging
import subprocess

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def absolute(p):
    return os.path.join(os.environ['CODEBUILD_SRC_DIR'], p)


def execute(c):
    logger.info('COMMAND ==> ' + c)
    c = subprocess.call(c, shell=True)
    logger.info('CODE ==> ' + str(c))
    return c


logger.info('Installing requirement...')
execute('pip3.6 install -r {} -t {}'.format(absolute('requirements.txt'), os.environ['CODEBUILD_SRC_DIR']))

logger.info('Zipping...')
execute('zip -q -j -r lambda_function.zip {}'.format(os.environ['CODEBUILD_SRC_DIR']))

config_file = absolute('_uploader/{}.json'.format(os.environ['BRANCH']))

if os.path.isfile(config_file):

    logger.info('Starting {}...'.format(os.environ['BRANCH'].capitalize()))

    config = dict(BRANCH=os.environ['BRANCH'], KEY=os.environ['KEY'], CONFIG_BUCKET=os.environ['CONFIG_BUCKET'])

    execute(
        'lambda-uploader'
        ' --no-build -c={} '
        '-s={} -k=lambda/lambda-uploader.zip '
        '--variables=\'{}\''.format(config_file, os.environ['ZAPPA_BUCKET'], json.dumps(config))
    )

else:
    execute('No {}.json found!'.format(os.environ['BRANCH']))
