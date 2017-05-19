#!/usr/bin/env bash
pip3 install --upgrade pip3
pip3 install virtualenv
virtualenv -p `which python3` venv
venv/bin/pip3 install --no-cache-dir -r requirements.txt
wget -O ./lambda.py $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py && python3 lambda.py