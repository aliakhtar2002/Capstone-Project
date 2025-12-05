# Variables for SOC project infrastructure
# These match our actual running instance

variable "aws_region" {
  description = "AWS Ohio region where our instance is"
  default = "us-east-2"
}

variable "instance_type" {
  description = "Same as our t3.medium instance"
  default = "t3.medium"
}

variable "key_name" {
  description = "Our SSH key name"
  default = "NEW CYBER KEY"
}

variable "ami_id" {
  description = "AMI ID from our running instance"
  default = "ami-0a5a5b7e2278263e5"
}
