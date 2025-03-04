#!/bin/bash

# Create users and groups if they do not exist
sudo useradd -m backend_dev
sudo useradd -m frontend_dev
sudo useradd -m db_admin
sudo useradd -m auditor
sudo groupadd dev_team
sudo groupadd db_team

# Add users to their respective groups
sudo usermod -aG dev_team backend_dev
sudo usermod -aG dev_team frontend_dev
sudo usermod -aG db_team db_admin

# Change ownership of directories
sudo chown backend_dev:dev_team /home/labDirectory/project/backend
sudo chown frontend_dev:dev_team /home/labDirectory/project/frontend
sudo chown db_admin:db_team /home/labDirectory/project/database

# Set permissions for directories
sudo chmod 750 /home/labDirectory/project/backend       # rwxr-x--- for backend
sudo chmod 740 /home/labDirectory/project/frontend     # rwxr----- for frontend
sudo chmod 700 /home/labDirectory/project/database     # rwx------ for database

# Grant sudo access to auditor for listing database directory
echo "auditor ALL=(ALL) NOPASSWD: /bin/ls /home/labDirectory/project/database" | sudo tee /etc/sudoers.d/auditor
sudo chmod 440 /etc/sudoers.d/auditor

echo "Configuration complete!"