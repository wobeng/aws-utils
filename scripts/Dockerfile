FROM ubuntu:16.10

# Install dependencies
RUN apt-get update -y

# Install python
RUN apt-get install -y  python3.6 python3.6-dev python3.6-venv wget
RUN  ln -s /usr/bin/python3.6 /usr/local/bin/python
RUN  ln -s /usr/bin/python3.6 /usr/local/bin/python3

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN ln -s /usr/local/bin/pip3.6 /usr/local/bin/pip3

# Install ffmpeg
RUN apt-get install -y  ffmpeg

# Install unoconv
RUN apt-get install -y unoconv

# Install awscli
RUN pip install awscli