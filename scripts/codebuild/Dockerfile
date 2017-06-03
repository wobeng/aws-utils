FROM amazonlinux

# Install dependencies
RUN yum-config-manager --enable epel
RUN yum update -y
RUN yum install -y gcc gcc-c++ make wget yum-utils groupinstall development zlib-devel openssl-devel git zip which

# Install python
RUN cd /usr/src
RUN wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
RUN tar xzf Python-3.6.1.tgz && rm Python-3.6.1.tgz
RUN cd Python-3.6.1 && ./configure && make altinstall

# Install NodeJs
RUN wget https://nodejs.org/dist/v6.10.3/node-v6.10.3.tar.gz
RUN tar -xvf node-v6.10.3.tar.gz && rm node-v6.10.3.tar.gz
RUN cd node-v6.10.3 && ./configure && make && make install

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN python3.6 get-pip.py

# Install awscli
RUN pip install awscli
RUN pip3.6 install awscli

# Install lambda-uploader
RUN pip install lambda-uploader
RUN pip3.6 install lambda-uploader

# Install virtualenv
RUN pip install virtualenv
RUN virtualenv -p python /tmp/venv2
RUN virtualenv -p python3.6 /tmp/venv3

# Activate npm
RUN npm install -g grunt-cli
RUN npm config set strict-ssl false

# Set Locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8