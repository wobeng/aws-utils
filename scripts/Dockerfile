FROM ubuntu:latest

# Install dependencies
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN add-apt-repository ppa:jonathonf/ffmpeg-3
RUN apt-get update -y
RUN apt-get install -y zip nodejs npm unoconv

# Install npm
RUN npm config set strict-ssl false
RUN npm install -g grunt-cli

# Install pip
RUN pip3.6 install --upgrade pip
RUN pip3.6 install lambda-uploader
RUN pip3.6 install virtualenv

# testing

CMD ["which", "python3.6"]
CMD ["which", "ffmpeg"]
CMD ["which", "nodejs"]
CMD ["which", "npm"]
CMD ["which","unoconv"]
CMD ["which", "pip3.6"]
CMD ["pip3.6", "list"]