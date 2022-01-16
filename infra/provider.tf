provider "aws" {
  region = var.aws_region
}

# centralizar o controle de estado do terraform

terraform {
  backend "s3" {
    bucket = "terraform-state-aws-project"
    key    = "state/pj/terraform.tfstate"
    region = "us-east-1"
  }
}