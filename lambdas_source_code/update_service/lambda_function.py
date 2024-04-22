import json
import boto3

ecs = boto3.client('ecs')

def lambda_handler(event, context):
    sns_message = json.dumps(event)
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    message_id = event['Records'][0]['Sns']['MessageId']
    queue_messages = sns_message.get('Queue_Messages')
    service_desired_count = sns_message.get('Service_desired_count')
    scaling_desired_count = sns_message.get('Scaling_Desired_Count')
    scaling_action = sns_message.get('Action')
    service_name = sns_message.get('Service')
    cluster_name = sns_message.get('Cluster')
    try:
        response = ecs.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=scaling_desired_count
        )
        logs =  {
            "Queue_Messages": queue_messages,
            "Service_desired_count": service_desired_count,
            "Scaling_Desired_Count": scaling_desired_count,
            "Action": scaling_action,
            "Service": service_name,
            "Cluster": cluster_name,
            "MessageID": message_id
        }
        print(logs)
    except Exception as err:
        print(f'Unable to update service: {err}')