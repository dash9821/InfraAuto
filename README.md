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

## Step 1:

Create an S3 bucket and DynamoDB table using terrraform and then configure terraform to use tham as its backend. The terraform code for the S3 bucket and DynamoDB table is present in `backend.tf`. Copy the file and ensure that the name you give to the bucket is globally unique. After that make sure that you've configured AWS CLI to use your AWS credentials by creating an access key with an admin user. 

Then you can run `terraform init`, this will download the latest plugin for aws and initialize a local backend. If you want to use a particular version of the aws plugin then mention it in the terraform block present in `provider.tf`.

After that you can run `terraform validate` to see that your terraform code is valid. This is an optional step.

Run `terraform plan` to see that the resource are getting created correctly. 

Run `terraform apply --auto-approve` to create the resources on your aws account.

Once this is done you can add the backend block to the terraform block in `provider.tf`, i.e.:

```
    backend "s3" {
        bucket         = "dashlearn-tfstate-s3-9821"
        key            = "global/tfstate/default/terraform.tfstate"
        region         = "ap-south-1"
        dynamodb_table = "state-lock"
    }
```
After adding this you have to run `terraform init -migrate-state` and you'll be prompted to move the existing state file over to the remote backend, type yes to move it to the S3 bucket. 

Once this is done you now have a remote backend for your terraform code which also has state locking which allows multiple users to work on the code and also preventing from conflicting code being executed on using state-locking.

## Step 2:

After setting up the remote backend now we can begin to create different workspaces for our different environments. Run the following commands:
```
terraform workspace new nonprod
terraform init

terraform workspace new staging
terraform init

terraform workspace new prod
terraform init

#To switch to other workspaces use terraform workspce select command.
```
Once you've initialized all the workspaces there'll be an empty tf-state file create in your S3 bucket at the path `env:/WORKSPACE/global/tfstate/default/terraform.tfstate`

## Step 3:

The directory structure of the terraform code looks like the following:

```
├── main.tf
├── provider.tf
├── default-vars.tf
├── modules
│   ├── EKS
│   │   └── eks.tf
│   │   └── eks-vars.tf
│   ├── EFS
│   │   └── efs.tf
│   │   └── efs-vars.tf
│   ├── ASG
│   │   └── asg.tf
│   │   └── asg-vars.tf
├── environments
│   ├── nonprod
│   │   └── vars.tf
│   ├── staging
│   │   └── vars.tf
│   └── prod
│       └── vars.tf
```

We'll be using modules to combine a few resources to make things a little less cluttered in our `main.tf` file. We'll call these modules by using the following code in our `main.tf` file:

```
module "eks" {
  source             = "./modules/EKS"
  cluster_name       = "my-eks-cluster"
  cluster_role_arn   = "arn:aws:iam::123456789012:role/EKSClusterRole"
  subnet_ids         = ["subnet-abcde123", "subnet-12345fgh"]
  node_group_name    = "my-eks-nodes"
  node_role_arn      = "arn:aws:iam::123456789012:role/EKSNodeRole"
  desired_capacity   = 3
  max_size           = 5
  min_size           = 1
}
```

