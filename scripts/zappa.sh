#!/usr/bin/env bash
pip install virtualenv
virtualenv -p `which python3` venv
venv/bin/pip install -r requirements.txt
wget -O ./zappa.py 'https://raw.githubusercontent.com/wobeng/aws-helper/master/scripts/zappa.py'
chmod u+x zappa.py && python3 zappa.py