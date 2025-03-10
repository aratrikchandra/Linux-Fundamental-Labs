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


def read_file(file_path):
    """Read the contents of a file and return it as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        return None


def verify_lowercase(student_output, expected_output):
    """Verify the lowercase transformation."""
    try:
        if student_output == expected_output:
            return True, "Output matches expected result."
        else:
            return False, "Output does not match expected result."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"


def verify_no_digits(student_output, expected_output):
    """Verify the removal of digits."""
    try:
        if student_output == expected_output:
            return True, "Output matches expected result."
        else:
            return False, "Output does not match expected result."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"


def verify_replace_colons(student_output, expected_output):
    """Verify the replacement of colons with hyphens."""
    try:
        if student_output == expected_output:
            return True, "Output matches expected result."
        else:
            return False, "Output does not match expected result."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"


def verify_squeeze_spaces(student_output, expected_output):
    """Verify the squeezing of consecutive spaces."""
    try:
        if student_output == expected_output:
            return True, "Output matches expected result."
        else:
            return False, "Output does not match expected result."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"


def main():
    overall = {"data": []}
    data = []

    # List of test cases
    test_cases = [
        {
            "testid": "Task 1: Convert Uppercase to Lowercase",
            "student_file": "lowercase.txt",
            "expected_file": "expected_lowercase.txt",
            "verify_function": verify_lowercase,
            "maximum_marks": 1
        },
        {
            "testid": "Task 2: Remove All Digits",
            "student_file": "no_digits.txt",
            "expected_file": "expected_no_digits.txt",
            "verify_function": verify_no_digits,
            "maximum_marks": 1
        },
        {
            "testid": "Task 3: Replace Colons with Hyphens",
            "student_file": "replace_colons.txt",
            "expected_file": "expected_replace_colons.txt",
            "verify_function": verify_replace_colons,
            "maximum_marks": 1
        },
        {
            "testid": "Task 4: Squeeze Consecutive Spaces",
            "student_file": "squeeze_spaces.txt",
            "expected_file": "expected_squeeze_spaces.txt",
            "verify_function": verify_squeeze_spaces,
            "maximum_marks": 1
        }
    ]

    # Execute the student's script
    student_script_output, student_script_error = execute_command("./submission.sh")
    if student_script_output is None:
        overall["data"] = [{
            "testid": "Execution of submission.sh",
            "status": "failure",
            "score": 0,
            "maximum marks": 0,
            "message": f"Error executing submission.sh: {student_script_error}"
        }]
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        return

    # Verify each task
    for test in test_cases:
        test_result = {
            "testid": test["testid"],
            "status": "failure",
            "score": 0,
            "maximum marks": test["maximum_marks"],
            "message": ""
        }

        # Read student's output file
        student_output = read_file(test["student_file"])
        if student_output is None:
            test_result["message"] = f"Error reading {test['student_file']}."
            data.append(test_result)
            continue

        # Read expected output file
        expected_output = read_file(test["expected_file"])
        if expected_output is None:
            test_result["message"] = f"Error reading {test['expected_file']}."
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