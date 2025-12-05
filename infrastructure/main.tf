# AWS setup for SOC project - Based on our actual EC2 instance
# This matches our running CPulse instance EXACTLY

# AWS provider for Ohio region
provider "aws" {
  region = "us-east-2"
}

# Security group with EXACT ports from our instance
resource "aws_security_group" "soc_sg" {
  name = "soc-project-sg"
  description = "Matches our launch-wizard-4 security group exactly"
  
  # Port 22 - SSH
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }
  
  # Port 80 - HTTP
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP web access"
  }
  
  # Port 443 - HTTPS
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS access"
  }
  
  # Port 5000 - Our API
  ingress {
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SOC API (Ali's API)"
  }
  
  # Port 8080 - Additional service
  ingress {
    from_port = 8080
    to_port = 8080
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Additional service port"
  }
  
  # All outbound traffic
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance matching CPulse
resource "aws_instance" "soc_server" {
  ami = "ami-0a5a5b7e2278263e5"
  instance_type = "t3.medium"
  vpc_security_group_ids = [aws_security_group.soc_sg.id]
  key_name = "NEW CYBER KEY"
  
  tags = {
    Name = "CPulse"
    Project = "Capstone-Project"
    Student = "aliakhtar2002"
  }
  
  user_data = <<-EOT
    #!/bin/bash
    echo "Setting up SOC server - aliakhtar2002"
    sudo yum update -y
    echo "Ready for deployment"
  EOT
}

output "server_ip" {
  value = aws_instance.soc_server.public_ip
}

output "ssh_command" {
  value = "ssh -i 'NEW CYBER KEY.pem' ec2-user@${aws_instance.soc_server.public_ip}"
}

output "api_endpoint" {
  value = "http://${aws_instance.soc_server.public_ip}:5000"
}
