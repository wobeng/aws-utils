import json
import logging
import subprocess
import time

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stages = []

with open(os.path.join(os.environ["CODEBUILD_SRC_DIR"], "zappa_settings.json")) as json_data:
    zappa = json.load(json_data)
    if "api" in zappa:
        stages.append("api")
    if "client" in zappa:
        stages.append("client")

for stage in stages:

    if os.environ["BRANCH"] != "master":
        stage = stage + "_" + os.environ["BRANCH"]

    logger.info('Sleeping for 30 seconds')
    time.sleep(30)

    logger.info('Trying to update zappa')
    stage_update = ". {}; zappa update {}".format(os.path.join(os.environ["CODEBUILD_SRC_DIR"], "venv/bin/activate"),
                                                  stage)
    logger.debug(stage_update)
    code = subprocess.call(stage_update, shell=True)
    logger.debug("CODE ==> " + str(code))

    if code != 0:
        logger.info('Update to zappa failed. Trying to deploy zappa')
        stage_deploy = ". {}; zappa deploy {}".format(
            os.path.join(os.environ["CODEBUILD_SRC_DIR"], "venv/bin/activate"), stage)
        logger.debug(stage_deploy)
        code = subprocess.call(stage_deploy, shell=True)
        logger.debug("CODE ==> " + str(code))

        if code != 0:
            logger.debug("{} update or deploy not found!".format(stage.capitalize()))
