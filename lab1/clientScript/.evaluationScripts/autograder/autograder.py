import json
import os
import subprocess
def execute_command(command):
    """Execute a shell command and return the output and error."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            executable='/bin/bash'  # Ensure using Bash shell
        )
        return result.stdout.strip(), None  # Return output and no error
    except subprocess.CalledProcessError as e:
        # Return no output and the error message
        return None, e.stderr.strip()


def extract_pids(output):
    """Extract PIDs from the output."""
    try:
        lines = output.splitlines()
        pids = []
        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            if parts:
                pids.append(parts[0])
        return set(pids)
    except Exception as e:
        return None

def verify_file1(output, expected_output):
    """Verify the output of file1.sh."""
    try:
        student_pids = extract_pids(output)
        expected_pids = extract_pids(expected_output)

        if student_pids is None or expected_pids is None:
            return False, "Error parsing output."

        # Check if PIDs match
        if student_pids != expected_pids:
            return False, "PIDs do not match."

        # Check if USER is "labuser"
        lines = output.splitlines()
        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            if len(parts) >= 2 and parts[1] != "labuser":
                return False, f"USER field is not 'labuser' for PID {parts[0]}."

        return True, "Output matches expected result."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"

def verify_file2(output, expected_output):
    """Verify the output of file2.sh."""
    try:
        student_pids = set(output.splitlines())
        expected_pids = set(expected_output.splitlines())

        if not student_pids or not expected_pids:
            return False, "Error parsing output."

        if student_pids == expected_pids:
            return True, "Output matches expected result."
        else:
            return False, "PIDs do not match."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"

def verify_file3(output, expected_output):
    """Verify the output of file3.sh."""
    try:
        student_pids = set(output.splitlines())
        expected_pids = set(expected_output.splitlines())

        if not student_pids or not expected_pids:
            return False, "Error parsing output."

        if student_pids == expected_pids:
            return True, "Output matches expected result."
        else:
            return False, "PIDs do not match."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"

def verify_file4(output, expected_output):
    """Verify the output of file4.sh."""
    try:
        student_pids = extract_pids(output)
        expected_pids = extract_pids(expected_output)

        if student_pids is None or expected_pids is None:
            return False, "Error parsing output."

        if student_pids != expected_pids:
            return False, "PIDs do not match."

        # Check if the output is sorted by CPU usage in descending order
        lines = output.splitlines()
        prev_cpu = float('inf')
        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            if len(parts) >= 2:
                try:
                    cpu = float(parts[1])
                except ValueError:
                    return False, f"Invalid CPU value: '{parts[1]}' for PID {parts[0]}."
                if cpu > prev_cpu:
                    return False, "Processes are not sorted in descending order by CPU usage."
                prev_cpu = cpu

        return True, "Output matches expected result."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"

def main():
    lab_directory_path = "./home/labDirectory"  # Update this if the lab files are in a specific directory
    overall = {"data": []}
    data = []

    # List of test cases
    test_cases = [
        {
            "testid": "Task 1: List Processes Owned by 'labuser'",
            "script": "file1.sh",
            "verify_function": verify_file1,
            "expected_command": "ps -u labuser -o pid",
            "maximum_marks": 1
        },
        {
            "testid": "Task 2: Find All Python Processes",
            "script": "file2.sh",
            "verify_function": verify_file2,
            "expected_command": "pgrep python3",
            "maximum_marks": 1
        },
        {
            "testid": "Task 3: Find All C Processes",
            "script": "file3.sh",
            "verify_function": verify_file3,
            "expected_command": "pgrep simple",
            "maximum_marks": 1
        },
        {
            "testid": "Task 4: Show Top 5 Processes Sorted by CPU Usage",
            "script": "file4.sh",
            "verify_function": verify_file4,
            "expected_command": "ps -eo pid,%cpu --sort=-%cpu | head -n 6",
            "maximum_marks": 1
        }
    ]

    for test in test_cases:
        test_result = {
            "testid": test["testid"],
            "status": "failure",
            "score": 0,
            "maximum marks": test["maximum_marks"],
            "message": ""
        }

        # Execute student's script
        student_output, error = execute_command(f"{lab_directory_path}{test['script']}")
        if student_output is None:
            test_result["message"] = f"Error executing {test['script']}: {error}"
            data.append(test_result)
            continue  # Move to the next test case

        # Execute expected command
        expected_output, expected_error = execute_command(test["expected_command"])
        if expected_output is None:
            test_result["message"] = f"Error executing expected command: {expected_error}"
            data.append(test_result)
            continue

        # Verify the output
        success, message = test["verify_function"](student_output, expected_output)
        if success:
            test_result["status"] = "success"
            test_result["score"] = test["maximum_marks"]
        test_result["message"] = message

        data.append(test_result)

    # Save the result to evaluate.json
    overall['data'] = data
    with open('../evaluate.json', 'w') as f:
        json.dump(overall, f, indent=4)

if __name__ == "__main__":
    main()
