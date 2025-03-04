#!/bin/bash

# Function to check if a user exists
user_exists() {
    id "$1" &>/dev/null
}

# Function to check if a group exists
group_exists() {
    getent group "$1" &>/dev/null
}

# Function to check directory ownership
check_ownership() {
    local dir=$1
    local expected_user=$2
    local expected_group=$3
    local actual_user=$(stat -c '%U' "$dir")
    local actual_group=$(stat -c '%G' "$dir")

    if [[ "$actual_user" != "$expected_user" || "$actual_group" != "$expected_group" ]]; then
        echo "ERROR: Ownership of $dir is incorrect. Expected: $expected_user:$expected_group, Found: $actual_user:$actual_group"
        return 1
    else
        echo "SUCCESS: Ownership of $dir is correct."
        return 0
    fi
}

# Function to check directory permissions
check_permissions() {
    local dir=$1
    local expected_perms=$2
    local actual_perms=$(stat -c '%A' "$dir")

    if [[ "$actual_perms" != "$expected_perms" ]]; then
        echo "ERROR: Permissions of $dir are incorrect. Expected: $expected_perms, Found: $actual_perms"
        return 1
    else
        echo "SUCCESS: Permissions of $dir are correct."
        return 0
    fi
}

# Function to check sudo privileges for auditor
check_sudo_privileges() {
    if sudo -l -U auditor | grep -q "NOPASSWD: /bin/ls /home/labDirectory/project/database"; then
        echo "SUCCESS: Auditor has the correct sudo privileges."
        return 0
    else
        echo "ERROR: Auditor does not have the correct sudo privileges."
        return 1
    fi
}

# Check if required users exist
for user in admin backend_dev frontend_dev db_admin auditor; do
    if ! user_exists "$user"; then
        echo "ERROR: User $user does not exist."
        exit 1
    else
        echo "SUCCESS: User $user exists."
    fi
done

# Check if required groups exist
for group in dev_team db_team; do
    if ! group_exists "$group"; then
        echo "ERROR: Group $group does not exist."
        exit 1
    else
        echo "SUCCESS: Group $group exists."
    fi
done

# Check if users are in the correct groups
if ! id -nG backend_dev | grep -qw "dev_team"; then
    echo "ERROR: User backend_dev is not in group dev_team."
    exit 1
else
    echo "SUCCESS: User backend_dev is in group dev_team."
fi

if ! id -nG frontend_dev | grep -qw "dev_team"; then
    echo "ERROR: User frontend_dev is not in group dev_team."
    exit 1
else
    echo "SUCCESS: User frontend_dev is in group dev_team."
fi

if ! id -nG db_admin | grep -qw "db_team"; then
    echo "ERROR: User db_admin is not in group db_team."
    exit 1
else
    echo "SUCCESS: User db_admin is in group db_team."
fi

# Check directory ownership
check_ownership "/home/labDirectory/project/backend" "backend_dev" "dev_team" || exit 1
check_ownership "/home/labDirectory/project/frontend" "frontend_dev" "dev_team" || exit 1
check_ownership "/home/labDirectory/project/database" "db_admin" "db_team" || exit 1

# Check directory permissions
check_permissions "/home/labDirectory/project/backend" "drwxr-x---" || exit 1
check_permissions "/home/labDirectory/project/frontend" "drwxr-----" || exit 1
check_permissions "/home/labDirectory/project/database" "drwx------" || exit 1

# Check sudo privileges for auditor
check_sudo_privileges || exit 1

echo "All checks passed! The student has completed the lab correctly."
exit 0