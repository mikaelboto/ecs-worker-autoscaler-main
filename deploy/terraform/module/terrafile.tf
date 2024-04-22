module "deploy_stack" {
    source = "../"
    bucket_name = "my-new-bucket"
    region = "us-east-1"
}