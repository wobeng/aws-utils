FROM amazonlinux

# Install dependencies
RUN yum-config-manager --enable epel
RUN yum update -y
RUN yum install -y gcc make wget yum-utils groupinstall development zlib-devel openssl-devel git zip which
RUN yum install nodejs npm --enablerepo=epel

# Install python
RUN cd /usr/src
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
RUN tar xzf Python-3.6.0.tgz
RUN cd Python-3.6.0 && ./configure && make altinstall
RUN rm Python-3.6.0.tgz

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# Install awscli
RUN pip install awscli

# Install lambda-uploader
RUN pip install lambda-uploader

# Install virtualenv
RUN pip install virtualenv
RUN virtualenv -p python /tmp/venv2
RUN virtualenv -p python3.6 /tmp/venv3

# Activate npm
RUN npm install -g grunt-cli
RUN npm config set strict-ssl false