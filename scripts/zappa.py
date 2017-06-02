#!/usr/bin/env python3.6
import json
import logging
import subprocess
import time

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def absolute(p):
    return os.path.join(os.environ['CODEBUILD_SRC_DIR'], p)


def log_code(c):
    logger.debug('CODE ==> ' + str(c))


logger.info('Creating environment')
code = subprocess.call('virtualenv -p python3.6 {}'.format(absolute('venv')), shell=True)
log_code(code)

logger.info('Install requirement')
code = subprocess.call('{} install -r {}'.format(absolute('venv/bin/pip'), absolute('requirements.txt')), shell=True)
log_code(code)

stages = []

with open(absolute('zappa_settings.json')) as json_data:
    zappa = json.load(json_data)
    if 'api' in zappa:
        stages.append('api')
    if 'client' in zappa:
        stages.append('client')

for stage in stages:

    if os.environ['BRANCH'] != 'master':
        stage = stage + '_' + os.environ['BRANCH']

    logger.info('Sleeping for 30 seconds')
    time.sleep(30)

    logger.info('Trying to update zappa')
    stage_update = '. {}; zappa update {}'.format(absolute('venv/bin/activate'),stage)
    logger.debug(stage_update)
    code = subprocess.call(stage_update, shell=True)
    log_code(code)

    if code != 0:
        logger.info('Update to zappa failed. Trying to deploy zappa')
        stage_deploy = '. {}; zappa deploy {}'.format(absolute('venv/bin/activate'), stage)
        logger.debug(stage_deploy)
        code = subprocess.call(stage_deploy, shell=True)
        log_code(code)

        if code != 0:
            logger.debug('{} update or deploy not found!'.format(stage.capitalize()))
