SHELL:=bash
aws_profile=default
aws_region=eu-west-2

default: help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: bootstrap
bootstrap: ## Bootstrap local environment for first use
	@make git-hooks
	make bootstrap-terraform

.PHONY: bootstrap-terraform
bootstrap-terraform: ## Bootstrap local environment for first use (terraform only)
	@{ \
		export AWS_PROFILE=$(aws_profile); \
		export AWS_REGION=$(aws_region); \
		python3 bootstrap.py; \
	}

.PHONY: git-hooks
git-hooks: ## Set up hooks in .githooks
	@git submodule update --init .githooks ; \
	git config core.hooksPath .githooks \

.PHONY: lambda-zip
lambda-zip: ## Make zip file for lambda
	@cd lambda/verify_lambda_build && \
	./build_verify_lambda.sh && \
	cd ../../
	
.PHONY: handbook-local
handbook-local: ## Run handbook with content locally
	cd burendo-handbook && \
	npm install && \
	npm run dev;
