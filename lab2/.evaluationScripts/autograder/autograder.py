#!/usr/bin/python3

import os
import pwd
import grp
import stat
import json
import subprocess

def get_user_groups(username):
    try:
        user_entry = pwd.getpwnam(username)
        group_ids = os.getgrouplist(user_entry.pw_name, user_entry.pw_gid)
        group_names = []
        for gid in group_ids:
            try:
                group = grp.getgrgid(gid)
                group_names.append(group.gr_name)
            except KeyError:
                pass
        return group_names
    except KeyError:
        return []

def check_users_exist():
    testid = 1
    try:
        users = ['admin', 'backend_dev', 'frontend_dev', 'db_admin', 'auditor']
        missing = []
        for user in users:
            try:
                pwd.getpwnam(user)
            except KeyError:
                missing.append(user)
        if not missing:
            return {
                "testid": testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "All required users exist."
            }
        else:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": f"Missing users: {', '.join(missing)}."
            }
    except Exception as e:
        return {
            "testid": testid,
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": f"Error checking users: {str(e)}"
        }

def check_groups_exist():
    testid = 2
    try:
        groups = ['dev_team', 'db_team']
        missing = []
        for group in groups:
            try:
                grp.getgrnam(group)
            except KeyError:
                missing.append(group)
        if not missing:
            return {
                "testid": testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "All required groups exist."
            }
        else:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": f"Missing groups: {', '.join(missing)}."
            }
    except Exception as e:
        return {
            "testid": testid,
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": f"Error checking groups: {str(e)}"
        }

def check_group_memberships():
    testid = 3
    try:
        expected = {
            'backend_dev': 'dev_team',
            'frontend_dev': 'dev_team',
            'db_admin': 'db_team'
        }
        errors = []
        for user, group in expected.items():
            # Check user exists
            try:
                pwd.getpwnam(user)
            except KeyError:
                errors.append(f"User {user} does not exist.")
                continue
                
            # Check group exists
            try:
                grp.getgrnam(group)
            except KeyError:
                errors.append(f"Group {group} does not exist.")
                continue

            # Get user's actual groups using id command
            try:
                output = subprocess.check_output(
                    ['id', '-Gn', user],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                actual_groups = output.strip().split()
            except subprocess.CalledProcessError as e:
                errors.append(f"Couldn't verify groups for {user}: {e.output}")
                continue

            # Verify membership
            if group not in actual_groups:
                errors.append(f"User {user} not in {group} (found in {actual_groups})")

        if not errors:
            return {
                "testid": testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "All users in correct groups."
            }
        else:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": " ".join(errors)
            }
            
    except Exception as e:
        return {
            "testid": testid,
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": f"Error checking memberships: {str(e)}"
        }
def check_directory_ownership():
    testid = 4
    try:
        directories = [
            ('/home/labDirectory/project/backend', 'backend_dev', 'dev_team'),
            ('/home/labDirectory/project/frontend', 'frontend_dev', 'dev_team'),
            ('/home/labDirectory/project/database', 'db_admin', 'db_team')
        ]
        errors = []
        for path, exp_user, exp_group in directories:
            try:
                st = os.stat(path)
            except Exception as e:
                errors.append(f"Error accessing {path}: {str(e)}")
                continue
            try:
                user = pwd.getpwuid(st.st_uid).pw_name
            except KeyError:
                user = str(st.st_uid)
            try:
                group = grp.getgrgid(st.st_gid).gr_name
            except KeyError:
                group = str(st.st_gid)
            if user != exp_user or group != exp_group:
                errors.append(f"{path} owner: {user}:{group} (expected {exp_user}:{exp_group})")
        if not errors:
            return {
                "testid": testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "Directory ownership correct."
            }
        else:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": " ".join(errors)
            }
    except Exception as e:
        return {
            "testid": testid,
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": f"Error checking ownership: {str(e)}"
        }

def check_directory_permissions():
    testid = 5
    try:
        directories = [
            ('/home/labDirectory/project/backend', 'drwxr-x---'),
            ('/home/labDirectory/project/frontend', 'drwxr-----'),
            ('/home/labDirectory/project/database', 'drwx------')
        ]
        errors = []
        for path, expected_mode in directories:
            try:
                st = os.stat(path)
                actual_mode = stat.filemode(st.st_mode)
                if actual_mode != expected_mode:
                    errors.append(f"{path} permissions: {actual_mode} (expected {expected_mode})")
            except Exception as e:
                errors.append(f"Error accessing {path}: {str(e)}")
        if not errors:
            return {
                "testid": testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "Directory permissions correct."
            }
        else:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": " ".join(errors)
            }
    except Exception as e:
        return {
            "testid": testid,
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": f"Error checking permissions: {str(e)}"
        }

def check_sudo_privileges():
    testid = 6
    try:
        result = subprocess.run(
            ['sudo', '-l', '-U', 'auditor'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": f"Sudo check failureed: {result.stderr}"
            }
        if 'NOPASSWD: /bin/ls /home/labDirectory/project/database' in result.stdout:
            return {
                "testid": testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "Sudo privileges configured correctly."
            }
        else:
            return {
                "testid": testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": "Missing required sudo privilege."
            }
    except Exception as e:
        return {
            "testid": testid,
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": f"Error checking sudo: {str(e)}"
        }

if __name__ == "__main__":
    print("Executing Submission")
    return_code = os.system("bash submission.sh")
    if return_code == 0:
        print("Submission executed successfully")
    else:
        print("Submission execution failureed")

    overall = {"data": []}
    tests = [
        check_users_exist,
        check_groups_exist,
        check_group_memberships,
        check_directory_ownership,
        check_directory_permissions,
        check_sudo_privileges
    ]

    for test in tests:
        try:
            overall["data"].append(test())
        except Exception as e:
            print(f"Error running test: {str(e)}")

    with open('../evaluate.json', 'w', encoding='utf-8') as f:
        json.dump(overall, f, indent=4)

    print("Evaluation completed!")