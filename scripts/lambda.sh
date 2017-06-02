#!/usr/bin/env bash

# Set the working directory
cd $CODEBUILD_SRC_DIR

# Install requirement
pip3.6 install -r requirements.txt -t .

# Zip file
zip -q -r lambda_function.zip .

# Get lambda python script
wget $SCRIPT_URL/scripts/lambda.py
chmod u+x lambda.py

# Run lambda python script
python3.6 lambda.py
