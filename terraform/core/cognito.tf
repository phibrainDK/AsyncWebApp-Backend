# TODO: add custom email messages via lambda triggers
# https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
# https://registry.terraform.io/providers/figma/aws-4-49-0/latest/docs/resources/cognito_user_pool#custom_email_sender
# https://medium.com/craftsmenltd/customizing-aws-cognito-verification-emails-with-html-using-aws-lambda-379b584d2112

resource "aws_cognito_user_pool" "cognito_user_pool" {
  name                = "${local.prefix}-cognito-user-pool"
  username_attributes = ["email"]
  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_message        = "Por favor, ingresa el siguiente código para confirmar y habilitar tu cuenta en WellDoneSolutions: {####}"
    email_subject        = "WellDoneSolutions: Verificación de la cuenta de WellDoneSolutions"
  }
  auto_verified_attributes = ["email"]

  # COGNITO_DEFAULT | DEVELOPER
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
    # from_email_address    = "WDSNotificator@appWDS.com" (Only for SES)
  }
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  username_configuration {
    case_sensitive = true
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    string_attribute_constraints {
      min_length = 3
      max_length = 256
    }
  }
}

resource "aws_cognito_user_pool_client" "cognito_user_pool_client" {
  name                                 = "app-${local.stage}-client"
  user_pool_id                         = aws_cognito_user_pool.cognito_user_pool.id
  allowed_oauth_flows_user_pool_client = true
  access_token_validity                = 5
  allowed_oauth_flows                  = ["implicit"]
  allowed_oauth_scopes                 = ["email", "openid", "aws.cognito.signin.user.admin", "profile"]
  supported_identity_providers         = ["COGNITO"]
  depends_on                           = [aws_cognito_user_pool.cognito_user_pool]
  explicit_auth_flows                  = ["ALLOW_USER_SRP_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_ADMIN_USER_PASSWORD_AUTH"]
  callback_urls                        = ["https://example.com/callback-${local.company}"]
}


resource "aws_cognito_user_pool_domain" "cognito_domain" {
  domain       = "${local.company}-app"
  user_pool_id = aws_cognito_user_pool.cognito_user_pool.id
}

resource "aws_api_gateway_authorizer" "cognito" {
  name            = "${local.prefix}-cognito-authorizer"
  rest_api_id     = aws_api_gateway_rest_api.app.id
  type            = "COGNITO_USER_POOLS"
  identity_source = "method.request.header.bearer"
  provider_arns   = [aws_cognito_user_pool.cognito_user_pool.arn]
}

resource "aws_api_gateway_rest_api" "app" {
  name        = "ApiGatewayRest-${local.prefix}-backend-api"
  description = "Terraform Serverless Application WellDoneSolutions App"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  parent_id   = aws_api_gateway_rest_api.app.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id          = aws_api_gateway_rest_api.app.id
  resource_id          = aws_api_gateway_resource.proxy.id
  http_method          = "ANY"
  authorization        = "COGNITO_USER_POOLS"
  authorizer_id        = aws_api_gateway_authorizer.cognito.id
  authorization_scopes = ["email"]
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn

  request_templates = {
    "application/json" = <<EOF
{
  "email": "$context.authorizer.claims.email",
  "custom_body" : $input.json('$')
}
EOF
  }
}

resource "aws_api_gateway_method" "proxy_root" {
  rest_api_id          = aws_api_gateway_rest_api.app.id
  resource_id          = aws_api_gateway_rest_api.app.root_resource_id
  http_method          = "ANY"
  authorization        = "COGNITO_USER_POOLS"
  authorizer_id        = aws_api_gateway_authorizer.cognito.id
  authorization_scopes = ["email"]
}

resource "aws_api_gateway_integration" "lambda_root" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  resource_id = aws_api_gateway_method.proxy_root.resource_id
  http_method = aws_api_gateway_method.proxy_root.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn

  request_templates = {
    "application/json" = <<EOF
{
  "email": "$context.authorizer.claims.email",
  "custom_body" : $input.json('$')
}
EOF
  }
}

resource "aws_api_gateway_deployment" "app" {
  depends_on = [
    aws_api_gateway_integration.lambda,
    aws_api_gateway_integration.lambda_root,
  ]

  rest_api_id = aws_api_gateway_rest_api.app.id
  stage_name  = "${local.stage}-tf"
}


resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.app.execution_arn}/*/*"
}

