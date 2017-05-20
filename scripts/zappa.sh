#!/usr/bin/env bash
pip install virtualenv
virtualenv -p `which python` venv
venv/bin/pip install -r requirements.txt
wget -O ./zappa.py $SCRIPT_URL/scripts/zappa.py
chmod u+x zappa.py && python zappa.py