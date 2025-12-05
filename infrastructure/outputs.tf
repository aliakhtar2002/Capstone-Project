# Outputs for SOC project

output "connection_info" {
  value = <<-EOT
  
  SOC Server Configuration (Matches CPulse):
  =========================================
  Instance: CPulse replica
  Type: t3.medium
  Region: us-east-2
  Key: NEW CYBER KEY
  
  Open Ports (EXACT match):
  ========================
  22 - SSH
  80 - HTTP
  443 - HTTPS
  5000 - SOC API
  8080 - Services
  
  Connect:
  =======
  SSH: ssh -i "NEW CYBER KEY.pem" ec2-user@${aws_instance.soc_server.public_ip}
  
  Access:
  =======
  API: http://${aws_instance.soc_server.public_ip}:5000
  HTTP: http://${aws_instance.soc_server.public_ip}
  HTTPS: https://${aws_instance.soc_server.public_ip}
  
  EOT
}
