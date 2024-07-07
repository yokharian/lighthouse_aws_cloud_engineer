import aws_cdk as core
import aws_cdk.assertions as assertions

from lighthouse_aws_cloud_engineer.lighthouse_aws_cloud_engineer_stack import LighthouseAwsCloudEngineerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lighthouse_aws_cloud_engineer/lighthouse_aws_cloud_engineer_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LighthouseAwsCloudEngineerStack(app, "lighthouse-aws-cloud-engineer")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
