from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_s3 as s3,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct


class DevopsCdkWebappStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 2 AZs, private subnets go through NAT to reach internet
        vpc = ec2.Vpc(
            self,
            "WebVpc",
            max_azs=2,
            nat_gateways=1
        )

        # private bucket, access only via pre-signed URLs
        bucket = s3.Bucket(
            self,
            "WebBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # tasks need read/write on S3 and permission to push logs to CloudWatch
        task_role = iam.Role(
            self,
            "TaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )
        bucket.grant_read_write(task_role)
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchAgentServerPolicy")
        )

        log_group = logs.LogGroup(
            self,
            "WebAppLogs",
            removal_policy=RemovalPolicy.DESTROY,
        )

        # only ports 80 and 443 should reach the load balancer
        alb_sg = ec2.SecurityGroup(
            self,
            "AlbSG",
            vpc=vpc,
            allow_all_outbound=True,
        )
        alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))
        alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443))

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FargateService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            public_load_balancer=True,
            security_groups=[alb_sg],
            task_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("."),
                container_port=80,
                task_role=task_role,
                log_driver=ecs.LogDrivers.aws_logs(
                    stream_prefix="webapp",
                    log_group=log_group,
                ),
            ),
        )

        # scale between 2 and 4 tasks based on CPU
        scaling = fargate_service.service.auto_scale_task_count(
            min_capacity=2,
            max_capacity=4,
        )
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=60,
        )

        CfnOutput(self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
        )
        CfnOutput(self, "BucketName",
            value=bucket.bucket_name,
        )
