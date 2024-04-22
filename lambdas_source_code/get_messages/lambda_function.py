import json
import boto3
import logging
import os

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
ecs = boto3.client('ecs')
sns = boto3.client('sns')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


topic_arn = os.environ['TOPIC_ARN']
bucket_name = os.environ['S3_BUCKET']
object_key = 'autoscaler_config.json'




def send_sns(queue_messages,service_desired_count,scaling_desired_count,scaling_action,service_name,cluster_name):
    message_body = {
        "Queue_Messages": queue_messages,
        "Service_desired_count": service_desired_count,
        "Scaling_Desired_Count": scaling_desired_count,
        "Action": scaling_action,
        "Service": service_name,
        "Cluster": cluster_name
    }
    message_json = json.dumps(message_body)
    response = sns.publish(
    TopicArn=topic_arn,
    Message=message_json
    )
    logs =  {
        "Queue_Messages": queue_messages,
        "Service_desired_count": service_desired_count,
        "Scaling_Desired_Count": scaling_desired_count,
        "Action": scaling_action,
        "Service": service_name,
        "Cluster": cluster_name,
        "MessageID": response['MessageId']
    }
    logger.info(logs)
    


def lambda_handler(event, context):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    json_data = json.loads(response['Body'].read().decode())


    for parsed_json in json_data['Services']:
        cluster_name = parsed_json['Cluster']
        service_name = parsed_json['Service']
        messages_per_worker = parsed_json['MessagesPerWorker']
        min_size = parsed_json['MinSize']
        max_size = parsed_json['MaxSize']
        queue_url = parsed_json['QueueUri']
        get_queue = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=[
                'All'
            ]
        )
        queue_messages = int(get_queue['Attributes']['ApproximateNumberOfMessages'])
        scaling_desired_count = queue_messages / messages_per_worker
        if scaling_desired_count < min_size or scaling_desired_count == min_size:
            scaling_desired_count = min_size
        else:
            scaling_desired_count = int(scaling_desired_count) + (scaling_desired_count % 1 > 0)
        if scaling_desired_count > max_size or scaling_desired_count == max_size:
            scaling_desired_count = max_size

        get_service = ecs.describe_services(
            cluster=cluster_name,
            services=[service_name]
            )

        for service in get_service['services']:
            service_desired_count = service['desiredCount']
            if scaling_desired_count == service_desired_count:
                scaling_action = "No action required"
                logs =  {
                    "Queue_Messages": queue_messages,
                    "Service_desired_count": service_desired_count,
                    "Scaling_Desired_Count": scaling_desired_count,
                    "Action": scaling_action,
                    "Service": service_name,
                    "Cluster": cluster_name
                }
                logger.info(logs)
    
            elif scaling_desired_count < service_desired_count:
                scaling_action = "Scaling down service"
                send_sns(queue_messages,service_desired_count,scaling_desired_count,scaling_action,service_name,cluster_name)      
            else:
                scaling_action = "Scaling up service"
                send_sns(queue_messages,service_desired_count,scaling_desired_count,scaling_action,service_name,cluster_name)
  
