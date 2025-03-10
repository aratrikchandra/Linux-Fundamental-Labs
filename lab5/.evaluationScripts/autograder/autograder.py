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

def verify_step1(output):
    """Verify the output of Step 1: View contents of tar archive."""
    expected_files = ["fold1/", "fold2/", "fold3/", "fold4/", "fold5/", 
                      "fold1/file1.txt", "fold2/file2.txt", "fold3/file3.txt", 
                      "fold4/file4.txt", "fold5/file5.txt"]
    
    # Split the output into a list of files
    output_files = output.strip().split('\n')
    
    # Check if all expected files are present
    for file in expected_files:
        if file not in output_files:
            return False, f"Expected file '{file}' not found in archive contents."

    # Check if there are any unexpected files
    for file in output_files:
        if file not in expected_files:
            return False, f"Unexpected file '{file}' found in archive contents."

    return True, "Step 1 completed successfully."

def verify_step2(output):
    """Verify the output of Step 2: Extract specific folders."""
    try:
        if not os.path.isdir("fold1") or not os.path.isdir("fold2") or os.path.isdir("fold3") or os.path.isdir("fold4") or os.path.isdir("fold5"):
            return False, "Folders were not extracted correctly."
        return True, "Step 2 completed successfully."
    except Exception as e:
        return False, f"Exception during verification: {str(e)}"

def verify_step3():
    """Verify the output of Step 3: Create new tar archives with different compression methods."""
    try:
        # List of expected files in each archive
        expected_files = ["fold1/", "fold2/", "readme.txt"]

        # Check for each compressed archive
        archives = [
            {"filename": "file.tgz", "compression": "gzip", "command": "tar -tzf"},
            {"filename": "file.tar.bz2", "compression": "bzip2", "command": "tar -tjf"},
            {"filename": "file.tar.xz", "compression": "xz", "command": "tar -tJf"}
        ]

        results = []
        total_marks = 0

        for archive in archives:
            filename = archive["filename"]
            command = archive["command"]
            compression = archive["compression"]

            # Check if the archive exists
            if not os.path.isfile(filename):
                results.append(f"{filename} does not exist.")
                continue

            # Verify the contents of the archive
            output, error = execute_command(f"{command} {filename}")
            if output is None:
                results.append(f"Error reading {filename}: {error}")
                continue

            # Check if all expected files are present
            missing_files = [file for file in expected_files if file not in output]
            if missing_files:
                results.append(f"{filename} is missing: {', '.join(missing_files)}")
            else:
                results.append(f"{filename} is correct and contains all required files.")
                total_marks += 1

        # Prepare the final message
        message = "\n".join(results)
        return total_marks, message

    except Exception as e:
        return 0, f"Exception during verification: {str(e)}"

def main():
    overall = {"data": []}
    data = []

    # List of test cases
    test_cases = [
        {
            "testid": "Task 1: View Contents of Tar Archive",
            "script": "./submission1.sh",
            "verify_function": verify_step1,
            "maximum_marks": 1
        },
        {
            "testid": "Task 2: Extract Specific Folders",
            "script": "./submission2.sh",
            "verify_function": verify_step2,
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
        student_output, error = execute_command(test['script'])
        if error:
            test_result["message"] = f"Error executing {test['script']}: {error}"
            data.append(test_result)
            continue  # Move to the next test case

        # Verify the output or result
        success, message = test["verify_function"](student_output if test["verify_function"] == verify_step1 else None)
        if success:
            test_result["status"] = "success"
            test_result["score"] = test["maximum_marks"]
        test_result["message"] = message

        data.append(test_result)

    # Test case for Step 3: Create new tar archives with different compression methods
    test_result = {
        "testid": "Task 3: Create New Tar Archives with Compression",
        "status": "failure",
        "score": 0,
        "maximum marks": 3,
        "message": ""
    }

    # Execute student's script
    student_output, error = execute_command("./submission3.sh")
    if error:
        test_result["message"] = f"Error executing submission3.sh: {error}"
        data.append(test_result)
    else:
        # Verify Step 3
        score, message = verify_step3()
        if score == 3:
            test_result["status"] = "success"
        test_result["score"] = score
        test_result["message"] = message

        data.append(test_result)
    # Save the result to evaluate.json
    overall['data'] = data
    with open('../evaluate.json', 'w') as f:
        json.dump(overall, f, indent=4)

if __name__ == "__main__":
    main()
