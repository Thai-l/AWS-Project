resource "aws_lambda_function" "lambdagetfiles" {
  # para subir de maneira automatizada precisa de um .zip sobe todas as libs
  filename      = "lambda_function_payload.zip"
  function_name = var.lambda_function_name
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 60

# Controle de estado do .zip
  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  runtime = "python3.8"
  
  tags = {
  Name   = "MyProjectAn",
  }

}