FROM ubuntu:latest as ubuntu-stage

# Install common packages
RUN apt-get update -y && apt-get install -y \
    software-properties-common \
    language-pack-en-base \
    debconf-utils \
    curl \
    net-tools \
    wget \
    nano \
    vim \
    less \
    iproute2 \
    python3 \
    python3-pip \
    man-db \
    sudo \
    tar \
    gzip \
    bzip2 \
    xz-utils

# Setup Environment variables
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM=xterm-256color

# Setup Directory Structure
RUN mkdir /home/labDirectory
RUN mkdir /home/.evaluationScripts

# Copy directories to the container
# COPY labDirectory /home/labDirectory
# COPY .evaluationScripts /home/.evaluationScripts


# Global Settings
RUN echo "cd /home/labDirectory" > /root/.bashrc && \
    echo "alias ls='ls --color=always'" >> /root/.bashrc && \
    echo "rm -f \`find /home -type f -name \"._*\"\`" >> /root/.bashrc

WORKDIR /home

# Default command to keep the container running
CMD [ "/bin/bash", "-c", "while :; do sleep 10; done" ]