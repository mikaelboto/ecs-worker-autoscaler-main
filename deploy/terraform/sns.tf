resource "aws_sns_topic" "update_topic" {
  name = "ecs-worker-autoscaler-topic-${var.region}"
}

resource "aws_lambda_permission" "sns_lambda_permission" {
  statement_id  = "sns-lambda-permission"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update.arn
  principal     = "sns.amazonaws.com"

  source_arn = aws_sns_topic.update_topic.arn
}

resource "aws_sns_topic_subscription" "sns_lambda_subscription" {
  topic_arn = aws_sns_topic.update_topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.update.arn
}