FROM amazonlinux

# Install dependencies
RUN yum update -y
RUN yum install -y gcc make wget yum-utils groupinstall development zlib-devel openssl-devel

# Install python
RUN cd /usr/src
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
RUN tar xzf Python-3.6.0.tgz
RUN cd Python-3.6.0 && ./configure && make altinstall
RUN rm Python-3.6.0.tgz

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

# Install lambda-uploader
RUN pip3.6 install lambda-uploader

# Set the working directory to /app
WORKDIR $CODEBUILD_SRC_DIR

# Install requirement
CMD pip3.6 install -r requirements.txt -t .

# zip file
CMD zip -q -r lambda_function.zip .

# get lambda python script
CMD wget $SCRIPT_URL/scripts/lambda.py
CMD chmod u+x lambda.py

# run lambda python script
CMD python3.6 lambda.py
