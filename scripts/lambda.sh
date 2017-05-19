#!/usr/bin/env bash
pip install virtualenv
virtualenv -p `which python3` venv
venv/bin/pip install --no-cache-dir -r requirements.txt
wget -O ./lambda.py $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py && python3 lambda.py