FROM ubuntu:16.10

# Install dependencies
RUN apt-get update -y
RUN apt-get install -y  ffmpeg unoconv python3.6 nodejs npm

# Install npm
RUN npm config set strict-ssl false
RUN npm install -g grunt-cli

# Install pip
RUN pip install --upgrade pip
RUN pip install awscli