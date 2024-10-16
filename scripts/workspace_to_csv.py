import sys

# Read workspaces from input
workspaces_input = sys.stdin.read().strip()

# Split the input into a list
workspaces_list = workspaces_input.split()

# Join the list with commas to create CSV format
csv_output = ','.join(workspaces_list)
print(csv_output)
