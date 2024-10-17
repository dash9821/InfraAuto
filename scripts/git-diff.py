import subprocess
import json
import os

def run_git_diff(branch_name):
    try:
        # Run git diff command
        diff = subprocess.check_output(
            ["git", "diff", "--name-only", branch_name],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip().splitlines()
        return diff
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e.output.decode('utf-8')}")
        return []

def get_environment_names():
    # List all environment directories
    envs_dir = 'environments'
    return [name for name in os.listdir(envs_dir) if os.path.isdir(os.path.join(envs_dir, name))]

def classify_changes(changed_files):
    environment_changes = set()  # Use a set to avoid duplicates
    common_code_changed = False

    for file in changed_files:
        # Check if the file is in the environments directory
        if file.startswith('environments/'):
            # Extract the environment name from the file path
            env_name = file.split('/')[1]  # Get the directory name
            environment_changes.add(env_name)  # Use a set to avoid duplicates

        # Check if the file is common code
        elif file in ['main.tf', 'provider.tf', 'default-vars.tf'] or \
            file.startswith('modules/'):
            common_code_changed = True

    return list(environment_changes), common_code_changed  # Convert back to list

def main():
    # Get the current branch name (assuming the script is run from within a git repo)
    branch_name = "main"  # Replace with the branch you want to compare against

    # Get the list of changed files
    changed_files = run_git_diff(branch_name)

    # Get the list of environment names
    all_environments = get_environment_names()

    # Classify the changes
    environment_changes, common_code_changed = classify_changes(changed_files)

    # Prepare JSON output
    output = {}

    if common_code_changed:
        # If there's any common code change, include all environments
        output = all_environments
    else:
        # If only environment changes, include those specifically
        output = environment_changes

    # Print the JSON output
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
