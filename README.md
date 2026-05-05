# Production-Grade DevOps Deployment using AWS CDK, ECS Fargate, and ECR

## Overview

This project implements a production-ready deployment of a containerized web application on AWS using Infrastructure as Code (IaC) with AWS CDK (Python). It follows modern DevOps principles including automation, scalability, security, and modular infrastructure design.

The application is containerized using Docker, stored in Amazon ECR, and deployed on ECS Fargate behind an Application Load Balancer (ALB) for high availability and fault tolerance.

---

## Architecture

Client
→ Route 53 (optional)
→ Application Load Balancer (ALB)
→ ECS Fargate Service (Multi-AZ)
→ Docker Containers
→ Amazon ECR (Image Repository)

Supporting Components:

* IAM Roles (least privilege access)
* Security Groups (controlled traffic flow)
* VPC (isolated networking)

---

## Key Features

* Infrastructure as Code using AWS CDK (Python)
* Fully containerized deployment using Docker
* Serverless container orchestration with ECS Fargate
* Application Load Balancer for traffic distribution
* ECR integration for container image lifecycle
* Multi-AZ deployment for high availability
* Secure IAM role-based access control
* Automated asset build and deployment via CDK

---

## Deployment Workflow

1. Application source is containerized using Docker
2. CDK synthesizes CloudFormation templates
3. Docker image is built and pushed to Amazon ECR
4. ECS Task Definition is created referencing ECR image
5. ECS Fargate Service is provisioned across subnets
6. ALB is configured with target groups and health checks
7. Service is exposed via public ALB DNS

---

## Project Structure

```
devops-cdk-webapp/
├── app/
│   └── index.html
├── devops_cdk_webapp/
│   └── devops_cdk_webapp_stack.py
├── Dockerfile
├── requirements.txt
├── cdk.json
└── README.md
```

---

## Prerequisites

* AWS CLI configured (`aws configure`)
* AWS CDK installed (`npm install -g aws-cdk`)
* Python 3.8+
* Docker installed and running

---

## Deployment Steps

```bash
# Install dependencies
pip install -r requirements.txt

# Bootstrap environment (one-time)
cdk bootstrap

# Synthesize CloudFormation
cdk synth

# Deploy stack
cdk deploy
```

---

## Accessing the Application

After deployment, the output will include:

* Load Balancer DNS URL

Open in browser:

```
http://devops-farga-ajjdodh55zxc-825563525.us-east-1.elb.amazonaws.com/
```

---

## Security Considerations

* Security Groups restrict inbound/outbound traffic
* IAM roles follow least privilege principle
* Containers run in isolated Fargate environment
* No direct SSH access (serverless architecture)

---

## Scalability

* ECS Fargate allows horizontal scaling of containers
* ALB distributes traffic efficiently
* Can be extended with Auto Scaling policies (CPU/Memory-based)

---

## Observability (Extendable)

* CloudWatch logs for container monitoring
* Metrics for CPU, memory, and request count
* Can integrate with alarms and dashboards

---

## CI/CD Integration (Pluggable)

This architecture is designed to integrate with CI/CD pipelines such as:

* GitHub Actions
* Jenkins
* AWS CodePipeline

Typical pipeline flow:
Code → Build → Docker Image → Push to ECR → CDK Deploy

---

## Cleanup

```bash
cdk destroy
```

---

## Future Enhancements

* Auto Scaling policies for ECS service
* HTTPS with ACM + Route 53
* Blue/Green deployments
* Multi-environment setup (dev/staging/prod)
* Observability dashboards with alerts

## Application Output
![App screenshot](screenshots/app.png)
---

## Author

Harish Reddy
DevOps Engineer | AWS | Kubernetes | CI/CD | Infrastructure as Code
