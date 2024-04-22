resource "aws_s3_object" "config_object" {
  bucket = var.bucket_name
  key    = "autoscaler_config.json"
  source = "../../../autoscaler_config/autoscaler_config.json"

  content_type = "text/plain"
  etag = filemd5("../../../autoscaler_config/autoscaler_config.json")
}