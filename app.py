#!/usr/bin/env python3
import os
import aws_cdk as cdk
from devops_cdk_webapp.devops_cdk_webapp_stack import DevopsCdkWebappStack

app = cdk.App()

DevopsCdkWebappStack(app, "DevopsCdkWebappStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()
