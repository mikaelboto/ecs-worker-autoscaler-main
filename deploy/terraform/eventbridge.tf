resource "aws_cloudwatch_event_rule" "scheduler" {
  name                = aws_lambda_function.scheduled.function_name
  description         = "Describe sqs queue every minute"
  schedule_expression = "rate(1 minute)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.scheduler.name
  arn  = aws_lambda_function.scheduled.arn
}