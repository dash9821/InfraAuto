terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.70.0"
    }
  }
  backend "s3" {
    bucket         = "dashlearn-tfstate-s3-9821"
    key            = "global/tfstate/default/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "state-lock"
  }
}

provider "aws" {
  region = "ap-south-1"
}