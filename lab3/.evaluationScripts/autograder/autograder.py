import json
import os
import subprocess
import shutil

def execute_command(command):
    """Execute a shell command and return the output and error."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            executable='/bin/bash'
        )
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.strip()

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def verify_cut(test_case_dir):
    """Verify part1.txt, part2.txt, part3.txt for a hidden test case."""
    marks = 0
    messages = []
    expected_part1 = read_file(f"{test_case_dir}/expected_part1.txt")
    student_part1 = read_file("part1.txt")
    expected_part2 = read_file(f"{test_case_dir}/expected_part2.txt")
    student_part2 = read_file("part2.txt")
    expected_part3 = read_file(f"{test_case_dir}/expected_part3.txt")
    student_part3 = read_file("part3.txt")

    if student_part1 == expected_part1:
        marks += 1
    else:
        messages.append("part1.txt incorrect")
    if student_part2 == expected_part2:
        marks += 1
    else:
        messages.append("part2.txt incorrect")
    if student_part3 == expected_part3:
        marks += 1
    else:
        messages.append("part3.txt incorrect")

    return marks, "; ".join(messages) if messages else "All cut files correct"

def verify_paste(test_case_dir):
    """Verify combined.txt for a hidden test case."""
    expected = read_file(f"{test_case_dir}/expected_combined.txt")
    student = read_file("combined.txt")
    if student == expected:
        return 2, "combined.txt correct"
    else:
        return 0, "combined.txt incorrect"

def verify_uniq(test_case_dir):
    """Verify deduped.txt for a hidden test case."""
    expected = read_file(f"{test_case_dir}/expected_deduped.txt")
    student = read_file("deduped.txt")
    if student == expected:
        return 2, "deduped.txt correct"
    else:
        return 0, "deduped.txt incorrect"

def verify_sort(test_case_dir):
    """Verify output.txt for a hidden test case."""
    expected = read_file(f"{test_case_dir}/expected_output.txt")
    student = read_file("output.txt")
    if student == expected:
        return 2, "output.txt correct"
    else:
        return 0, "output.txt incorrect"

def main():
    current_directory = os.getcwd()
    hidden_test_cases = ["hidden_test_case_1", "hidden_test_case_2"]
    overall = {"data": []}
    data = []

    # Define test cases (4 tasks: cut, paste, uniq, sort)
    test_cases = [
        {
            "testid": "Verify cut command",
            "verify_function": verify_cut,
            "maximum_marks": 6
        },
        {
            "testid": "Verify paste command",
            "verify_function": verify_paste,
            "maximum_marks": 4
        },
        {
            "testid": "Verify uniq command",
            "verify_function": verify_uniq,
            "maximum_marks": 4
        },
        {
            "testid": "Verify sort command",
            "verify_function": verify_sort,
            "maximum_marks": 4
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

        total_marks = 0
        all_messages = []

        # Check against both hidden test cases
        for test_case_dir in hidden_test_cases:
            # Copy hidden test case files to current directory
            hidden_dir = os.path.join(current_directory, test_case_dir)
            for file in ["employees1.txt", "employees2.txt", "employees3.txt"]:
                src = os.path.join(hidden_dir, file)
                dest = os.path.join(current_directory, file)
                shutil.copy(src, dest)

            # Run student's script
            student_script = os.path.join(current_directory, "submission.sh")
            _, error = execute_command(f"bash {student_script}")
            if error:
                all_messages.append(f"Error in {test_case_dir}: {error}")
                continue

            # Verify the task for this hidden test case
            marks, msg = test["verify_function"](hidden_dir)
            total_marks += marks
            all_messages.append(f"{test_case_dir}: {msg}")

        # Calculate score
        test_result["score"] = total_marks
        if total_marks >= test["maximum_marks"]:
            test_result["status"] = "success"
        test_result["message"] = "; ".join(all_messages)
        data.append(test_result)

    overall['data'] = data
    with open('../evaluate.json', 'w') as f:
        json.dump(overall, f, indent=4)
if __name__ == "__main__":
    main()