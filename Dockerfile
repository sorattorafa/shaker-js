FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update

# Python support
RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pytest colorama requests

# Java/Maven support
#RUN apt-get install -y openjdk-8-jdk
#RUN apt-get install -y maven
#RUN apt-get install -y nodejs npm

## instal nodejs and npm on a version
ENV NODE_VERSION=18.16.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version
RUN npm i -g yarn
#RUN apt install node-gyp
# stress-ng
RUN apt-get install -y stress-ng

COPY shaker /__shaker
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
