FROM ubuntu:16.10

# Install dependencies
RUN apt-get update -y

# Install python
RUN apt-get install -y  python3.6 python3.6-dev python3.6-venv wget

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

# Install imagemagick
RUN apt-get install -y imagemagick

# Install ffmpeg
RUN apt-get install -y  ffmpeg

# Install unoconv
RUN apt-get install -y unoconv

# Install awscli
RUN pip install awscli