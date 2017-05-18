import json
import subprocess

import os

CONFIG_FILE = "{}/_uploader/{}.json".format(os.environ["CODEBUILD_SRC_DIR"], os.environ["BRANCH"])

if os.path.isfile(CONFIG_FILE):

    config = dict(BRANCH=os.environ["BRANCH"], KEY=os.environ["KEY"], CONFIG_BUCKET=os.environ["CONFIG_BUCKET"])

    command = "lambda-uploader " \
              "-c={0}/_uploader/{1}.json " \
              "-s={2} " \
              "--virtualenv={0}/venv" \
              "-k=lambda/lambda-uploader.zip " \
              "--variables='{3}'".format(os.environ["CODEBUILD_SRC_DIR"], os.environ["BRANCH"],
                                         os.environ["ZAPPA_BUCKET"], json.dumps(config))
    print(command)
    subprocess.call(command, shell=True)

else:
    subprocess.call("No {}.json found!".format(os.environ["BRANCH"]), shell=True)
