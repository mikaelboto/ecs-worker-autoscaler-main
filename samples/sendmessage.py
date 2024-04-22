import boto3


sqs = boto3.client('sqs')

while True:
    queue_url = 'https://sqs.us-east-1.amazonaws.com/12345678900/helloworld'
    response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='Hello, world!'
    )

    print('Message ID:', response['MessageId'])
