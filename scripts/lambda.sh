#!/usr/bin/env bash
apt-get -y install zip
pip install lambda-uploader
pip install -r requirements.txt -t .
zip -r lambda_function.zip .
wget -O ./lambda.py $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py && python lambda.py

