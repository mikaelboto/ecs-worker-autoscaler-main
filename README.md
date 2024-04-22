## ECS WORKER AUTOSCALER

Scale ECS service based on amount of messages in SQS queues, scaling in and out tasks on demand.

## How it works

This repo deploys a S3 Bucket, couple lambda functions triggered by EventBridge and SNS topic to describe SQS queues every minute to manage ECS services desired count based on approximate number of messages in queue and the number of workers required to process them.


![Screenshot from 2023-05-09 21-52-21](https://github.com/chnacib/ecs-worker-autoscaler/assets/84737230/34981eed-83e8-4daa-8220-497a9a8bbd6b)



## How to configure


You need to set the Cluster name, Service name, amount of messages a worker can process, MinSize, MaxSize and QueueURI editing [/autoscaler_config/autoscaler_config.json](/autoscaler_config/autoscaler_config.json)

```
{
    "Services": [
        {
            "Cluster": "example",
            "Service": "example",
            "MessagesPerWorker": 250,
            "MinSize": 1,
            "MaxSize": 2,
            "QueueUri": "https://sqs.us-east-1.amazonaws.com/0123456789/helloworld"
        } 
    ]
}

```

If you have more than one service to apply this stack, edit the json file like this:


```
{
    "Services": [
        {
            "Cluster": "example",
            "Service": "example",
            "MessagesPerWorker": 250,
            "MinSize": 1,
            "MaxSize": 2,
            "QueueUri": "https://sqs.us-east-1.amazonaws.com/0123456789/helloworld"
        },
        {
            "Cluster": "example2",
            "Service": "example2",
            "MessagesPerWorker": 200,
            "MinSize": 1,
            "MaxSize": 4,
            "QueueUri": "https://sqs.us-east-1.amazonaws.com/0123456789/anotherqueue"
        } 
    ]
}

```

## Deploy 

To deploy this stack you must have terraform installed. If you don't, click this [link](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

```
git clone https://github.com/chnacib/ecs-worker-autoscaler.git
cd ./ecs-worker-autoscaler/deploy/terraform/module
```

Edit terrafile.tf and replace variables in module

```
module "deploy_stack" {
    source = "../"
    bucket_name = "my-new-bucket-name"
    region = "us-east-1"
}
```

Deploy terraform module

```
terraform init
terraform plan
terraform apply -auto-approve
```

## Testing 

To test this stack, deploy a sample image like nginx in ECS and a SQS queue. After apply terraform, in [/samples/](/samples/) you have 2 python scripts to send message or delete messages, just need to replace "queue_url" variable. 

```
queue_url = 'https://sqs.us-east-1.amazonaws.com/12345678900/helloworld'
```

after setup aws credentials by  ```aws configure```
, execute python scripts to send or delete messages

```
python3 sendmessage.py
```

```
python3 deletemessage.py
```


## Enjoy!!



![a68](https://github.com/chnacib/ecs-worker-autoscaler/assets/84737230/12e24527-aeba-4f67-bfbf-4f3a7d1e5d6a)








