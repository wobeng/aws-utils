FROM amazonlinux

# Install dependencies
RUN yum update -y
RUN yum install -y gcc make wget yum-utils groupinstall development zlib-devel openssl-devel git zip

# Install python
RUN cd /usr/src
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
RUN tar xzf Python-3.6.0.tgz
RUN cd Python-3.6.0 && ./configure && make altinstall
RUN rm Python-3.6.0.tgz

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

# Install virtualenv
RUN pip3.6 install virtualenv