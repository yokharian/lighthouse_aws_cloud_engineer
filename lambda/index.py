import os
import boto3


def handler(event, context):
    ecs = boto3.client('ecs')
    cluster_name = os.environ['CLUSTER_NAME']
    service_name = os.environ['SERVICE_NAME']

    response = ecs.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=0
    )

    print('ECS Service scaled down successfully:', response)
