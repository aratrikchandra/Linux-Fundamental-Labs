FROM ubuntu:latest as ubuntu-stage

# Installing common packages
RUN yes | unminimize
RUN apt-get update -y && apt-get install -y software-properties-common language-pack-en-base debconf-utils curl 
RUN apt-get update -y && apt-get install net-tools wget nano vim less -y
RUN apt-get update -y && apt-get install iproute2 python3 python3-pip -y

# Install anything you want here:
RUN apt-get install -y man-db

# Setup Environment variables
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM=xterm-256color

# Setup Directory Structure
RUN mkdir -p /home/labDirectory
RUN mkdir -p /home/.evaluationScripts
RUN mkdir -p /home/labuser/init_scripts

# Global Settings
RUN echo "cd /home/labDirectory" > /root/.bashrc
RUN echo "alias ls='ls --color=always'" >> /root/.bashrc
RUN echo "rm -f \`find /home -type f -name \"._*\"\`" >> /root/.bashrc

# Add a user for the lab
RUN useradd -ms /bin/bash labuser

# Switch to the root user to run the other processes
USER root
WORKDIR /root

# Download initialization scripts to the container
RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1FLcdqsyEOmboCnfuljBtPe3oHmt9qy9W' -O /home/labuser/init_scripts.tar.gz
RUN tar --strip-components=1 -xzf /home/labuser/init_scripts.tar.gz -C /home/labuser/init_scripts  # Extract to the correct directory

# Verify the extraction step
RUN ls -l /home/labuser/init_scripts

# Set permissions for the scripts
RUN chmod +x /home/labuser/init_scripts/*.sh

# Default command to keep the container running and start all processes
CMD ["/bin/bash", "-c", "/home/labuser/init_scripts/start_all.sh && su - labuser -c /home/labuser/init_scripts/start_dummy_processes.sh && /bin/bash"]
