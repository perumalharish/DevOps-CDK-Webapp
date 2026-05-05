from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct


class DevopsCdkWebappStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self,
            "WebVpc",
            max_azs=2,
            nat_gateways=1
        )

        # S3 Bucket
        bucket = s3.Bucket(
            self,
            "WebBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # ECS Cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # IAM Role
        task_role = iam.Role(
            self,
            "TaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        bucket.grant_read_write(task_role)

        # Fargate Service + ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FargateService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            public_load_balancer=True,
            task_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("."),
                container_port=80,
                task_role=task_role,
            ),
        )

        # Auto Scaling
        scaling = fargate_service.service.auto_scale_task_count(
            min_capacity=2,
            max_capacity=4,
        )

        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=60,
        )

        # Outputs
        CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
        )

        CfnOutput(
            self,
            "BucketName",
            value=bucket.bucket_name,
        )
# CfnOutput(
#     self,
#     "LoadBalancerDNS",
#     value=fargate_service.load_balancer.load_balancer_dns_name,
# )

# CfnOutput(
#     self,
#     "BucketName",
#     value=bucket.bucket_name,
# )