from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam
)
from constructs import Construct

class LighthouseAwsCloudEngineerStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Define a Fargate task definition with a single container
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef")

        container = task_definition.add_container(
            "DefaultContainer",
            image=ecs.ContainerImage.from_registry("public.ecr.aws/ecs-sample-image/amazon-ecs-sample:latest"),
            memory_limit_mib=512,
            cpu=256,
        )

        container.add_port_mappings(
            ecs.PortMapping(container_port=80)
        )

        # Define a Fargate service
        ecs_service = ecs.FargateService(
            self, "Service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            assign_public_ip=True
        )

        # Define the Lambda function
        scale_down_function = _lambda.Function(
            self, "ScaleDownFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'CLUSTER_NAME': cluster.cluster_name,
                'SERVICE_NAME': ecs_service.service_name
            }
        )

        # Add permissions for the Lambda to scale down the ECS service
        scale_down_function.add_to_role_policy(iam.PolicyStatement(
            actions=["ecs:UpdateService"],
            resources=[ecs_service.service_arn]
        ))

        # Define the EventBridge rule
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(minute="0", hour="23")
        )

        rule.add_target(targets.LambdaFunction(scale_down_function))
