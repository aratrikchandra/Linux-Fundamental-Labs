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
    sudo

# Setup Environment variables
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM=xterm-256color

# Setup Directory Structure
RUN mkdir /home/labDirectory
RUN mkdir -p /home/labDirectory/project
RUN mkdir -p /home/labDirectory/project/backend
RUN mkdir -p /home/labDirectory/project/frontend
RUN mkdir -p /home/labDirectory/project/database
RUN mkdir /home/.evaluationScripts

# Create dummy files in subdirectories
RUN echo "Backend dummy content" > /home/labDirectory/project/backend/backend_file.txt
RUN echo "Frontend dummy content" > /home/labDirectory/project/frontend/frontend_file.txt
RUN echo "Database dummy content" > /home/labDirectory/project/database/database_file.txt

# Create admin user
RUN useradd -m admin

# Set ownership of the project directory and subdirectories
RUN chown -R admin:admin /home/labDirectory/project

# Global Settings
RUN echo "cd /home/labDirectory" > /root/.bashrc && \
    echo "alias ls='ls --color=always'" >> /root/.bashrc && \
    echo "rm -f \`find /home -type f -name \"._*\"\`" >> /root/.bashrc

# Switch to the root user to run the other processes
USER root
WORKDIR /root

# Default command to keep the container running
CMD ["/bin/bash"]