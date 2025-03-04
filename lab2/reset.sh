#!/bin/bash

# Remove users and groups if they exist
sudo userdel -r backend_dev
sudo userdel -r frontend_dev
sudo userdel -r db_admin
sudo userdel -r auditor
sudo groupdel dev_team
sudo groupdel db_team

# Reset directory ownership and permissions
sudo chown root:root /home/labDirectory/project/backend
sudo chown root:root /home/labDirectory/project/frontend
sudo chown root:root /home/labDirectory/project/database
sudo chmod 755 /home/labDirectory/project/backend       # rwxr-xr-x for backend
sudo chmod 755 /home/labDirectory/project/frontend      # rwxr-xr-x for frontend
sudo chmod 755 /home/labDirectory/project/database      # rwxr-xr-x for database

# Remove sudo access for auditor
sudo rm /etc/sudoers.d/auditor

echo "Reset complete!"
