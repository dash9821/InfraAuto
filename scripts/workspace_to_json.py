import json
import sys

# Read workspaces from input
workspaces_input = sys.stdin.read().strip()

# Split the input into a list and create a JSON array
workspaces_list = workspaces_input.split()
print(json.dumps(workspaces_list))
