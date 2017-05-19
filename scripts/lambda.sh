#!/usr/bin/env bash
pip install virtualenv
virtualenv  venv
venv/bin/pip install -r requirements.txt
wget -O ./lambda.py $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py && python lambda.py
