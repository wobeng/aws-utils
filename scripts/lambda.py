#!/usr/bin/env python3.6
import json
import logging
import subprocess

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def absolute(p):
    return os.path.join(os.environ['CODEBUILD_SRC_DIR'], p)


def log_code(c):
    logger.debug('CODE ==> ' + str(c))


logger.info('Install requirement')
code = subprocess.call('pip3.6 install -r {} -t {}'.format(absolute('requirements.txt'), absolute('')),
                       shell=True)
log_code(code)

logger.info('Zipping...')
code = subprocess.call('zip -q -r lambda_function.zip {}'.format(absolute('')), shell=True)
log_code(code)

config_file = absolute('_uploader/{}.json'.format(os.environ['BRANCH']))

if os.path.isfile(config_file):

    logger.info('Starting {}'.format(os.environ['BRANCH'].capitalize()))

    config = dict(BRANCH=os.environ['BRANCH'], KEY=os.environ['KEY'], CONFIG_BUCKET=os.environ['CONFIG_BUCKET'])

    command = 'lambda-uploader --no-build -c={} -s={} -k=lambda/lambda-uploader.zip --variables="{}'''.format(
        config_file, os.environ['ZAPPA_BUCKET'], json.dumps(config))
    logger.debug(command)
    code = subprocess.call(command, shell=True)
else:
    code = subprocess.call('No {}.json found!'.format(os.environ['BRANCH']), shell=True)

log_code(code)
