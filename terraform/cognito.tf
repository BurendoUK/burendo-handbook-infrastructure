resource "aws_cognito_user_pool" "burendo" {
  name                     = "Burendo"
  auto_verified_attributes = ["email"]
}

resource "aws_cognito_identity_provider" "burendo_provider" {
  user_pool_id  = aws_cognito_user_pool.burendo.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    authorize_scopes              = "email openid profile"
    client_id                     = var.client_id
    client_secret                 = var.client_secret
    attributes_url                = "https://people.googleapis.com/v1/people/me?personFields="
    attributes_url_add_attributes = "true"
    authorize_url                 = "https://accounts.google.com/o/oauth2/v2/auth"
    oidc_issuer                   = "https://accounts.google.com"
    token_request_method          = "POST"
    token_url                     = "https://www.googleapis.com/oauth2/v4/token"
  }

  attribute_mapping = {
    email    = "email",
    username = "sub"
  }
}

resource "aws_cognito_user_pool_client" "burendo_client" {
  name = "burendo client"

  user_pool_id                         = aws_cognito_user_pool.burendo.id
  callback_urls                        = ["https://${local.environment_domain[local.environment]}"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["implicit"]
  allowed_oauth_scopes                 = ["email", "openid", "profile"]
  supported_identity_providers         = ["Google"]
}

resource "aws_cognito_user_pool_domain" "burendo_domain" {
  domain       = "burendo-domain"
  user_pool_id = aws_cognito_user_pool.burendo.id
}
