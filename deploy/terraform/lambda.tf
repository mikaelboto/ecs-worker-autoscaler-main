resource "aws_lambda_function" "scheduled" {
  filename      = "../../../lambda_functions/get_messages/get_messages.zip"
  function_name = "ecs-worker-autoscaler-scheduled-${var.region}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30
  memory_size   = 128

  environment {
    variables = {
      S3_BUCKET = var.bucket_name
      TOPIC_ARN = aws_sns_topic.update_topic.arn
    }
  }
}

resource "aws_lambda_function" "update" {
  filename      = "../../../lambda_functions/update_service/update_service.zip"
  function_name = "ecs-worker-autoscaler-update-${var.region}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30
  memory_size   = 128
}


resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.scheduled.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.scheduler.arn
}