#!/usr/bin/env bash
sudo apt-get update && apt-get -y install zip
pip install --upgrade pip && pip install lambda-uploader && pip install -r requirements.txt -t .
zip -q -r lambda_function.zip .
wget -O ./lambda.py $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py && python lambda.py

