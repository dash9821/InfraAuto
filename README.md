# InfraAuto
Create/Delete/Update AWS infra using GitHub actions.

We'll use terraform with backend on AWS to have a safe place to store all the state files.
All the code will use AWS modules itself no need to write our own modules. We can write defaults for everything in vars.tf
To setup multiple enviroments with the same terraform code we'll use terraform workspaces.

GitHub actions will be used to run terrafrom commands to work with the infrastructure. 
When a PR is raised terraform plan will run. All envs will have their own terraform plan job. 
The plan will be saved locally on the runner itself and will be used in the apply workflow.
When the PR is merged another worflow will be triggered to run terraform apply. There will be seperate jobs for all envs as before.

In addition we'll have a trigger build file in the root directory to trigger a the workflow whenever necessary,
We'll have a workflow to replace resources as well. It'll take a list of strings as input, the strings will be in the type "aws_type.name"
We'll use patch_env.tf to basically patch any resource values for each env seperately.

We'll create modules for grouping things up like everything required for EKS, including the addons for EFS, EBS.
We'll also work on setting up Disaster Recovery so by running a single workflow we can fail over to another region with minimal downtime. 