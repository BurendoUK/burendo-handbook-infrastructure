resource "null_resource" "download_package" {
  triggers = {
    downloaded = local.downloaded
  }

  provisioner "local-exec" {
    command = "curl -L -o ${local.downloaded} ${local.package_url}"
  }
}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "4.0.2"

  function_name = "${random_pet.this.id}-lambda"
  description   = "My awesome lambda function"
  handler       = "index.lambda_handler"
  runtime       = "python3.8"

  publish        = true
  lambda_at_edge = true

  create_package         = false
  local_existing_package = local.downloaded

  # @todo: Missing CloudFront as allowed_triggers?

  #    allowed_triggers = {
  #      AllowExecutionFromAPIGateway = {
  #        service = "apigateway"
  #        arn     = module.api_gateway.apigatewayv2_api_execution_arn
  #      }
  #    }
}
