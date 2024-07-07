#!/usr/bin/env python3
import aws_cdk as cdk
from lighthouse_aws_cloud_engineer.lighthouse_aws_cloud_engineer_stack import LighthouseAwsCloudEngineerStack

app = cdk.App()
LighthouseAwsCloudEngineerStack(app, "LighthouseAwsCloudEngineerStack")

app.synth()
