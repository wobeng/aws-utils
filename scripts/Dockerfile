FROM ubuntu:latest

# Install dependencies
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y
RUN apt-get install -y  ffmpeg unoconv python3.6

# Install npm
RUN npm config set strict-ssl false
RUN npm install -g grunt-cli

# Install pip
RUN pip install --upgrade pip
RUN pip install awscli
