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
bootstrap-terraform: ## Bootstrap local environment for first use
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
	@cd lambda && \
	rm -rf verify/ && \
	pip3 install --platform manylinux2014_x86_64 --implementation cp --python 3.9 --no-cache-dir --only-binary=:all: --upgrade --target verify cryptography==38.0.3 && \
	pip3 install -r requirements.txt --no-cache-dir --target verify && \
	cd verify && \
	zip -9 -r verify.zip . && \
	cd ../ && \
	zip -9 -r verify/verify.zip verify_code_lambda.py
	
.PHONY: handbook-local-public
handbook-local: ## Run handbook locally
	@cd burendo-handbook && \
	mv docusaurus.config.public.js docusaurus.config.js
	npm install && \
	npm run-script docusaurus start
	
.PHONY: handbook-local-private
handbook-local: ## Run handbook locally
	@cd burendo-handbook && \
	mv docusaurus.config.private.js docusaurus.config.js
	npm install && \
	npm run-script docusaurus start
