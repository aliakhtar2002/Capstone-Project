# Infrastructure as Code - SOC Project

## Exact Configuration
This Terraform creates an EC2 instance matching our CPulse server:

- **Region**: us-east-2 (Ohio)
- **Instance**: t3.medium
- **AMI**: ami-0a5a5b7e2278263e5
- **Key**: NEW CYBER KEY
- **Ports**: 22, 80, 443, 5000, 8080 (EXACT from our instance)

## Files
- main.tf - Main configuration
- variables.tf - Variables
- outputs.tf - Output info

## Usage
1. terraform init
2. terraform plan
3. terraform apply

## Note
This matches our actual CPulse instance security group.
For demo, we manually set up our instance.
