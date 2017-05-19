#!/usr/bin/env bash

mkdir lambda_function

shopt -s extglob dotglob
mv !lambda_function lambda_function
shopt -u dotglob

ls
ls lambda_function

venv/bin/pip3 install --no-cache-dir -r requirements.txt -t lambda_function
ls
wget -O ./lambda.py $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py && python3 lambda.py