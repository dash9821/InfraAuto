terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "5.70.0"
        }
    }
    backend "s3" {
        bucket = "dashlearn-tfstate-s3-9821"
        dynamodb_table = "state-lock"
        key = "global/tfstate/terraform.tfstate"
        region = "ap-south-1"
        encrypt = true
    }
}

provider "aws" {
    region = "ap-south-1"
}