FROM ubuntu:16.10

# Install dependencies
RUN apt-get update -y
RUN apt-get install -y  ffmpeg unoconv python3.6 python3.6-dev python3.6-venv wget

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
RUN pip3.6 install --upgrade pip
RUN pip3.6 install awscli
