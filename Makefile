.PHONY: all

.DEFAULT_GOAL: help

help: ## Shows this help
	@fgrep -h "##" $(MAKEFILE_LIST) | \
		fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build the Docker images
	@docker build -t $(QUAY_TAG):$(shell cat VERSION) .
	@docker build -t $(LOCAL_TAG):$(shell cat VERSION) .

push: ## Push the Docker images
	@docker push $(QUAY_TAG):$(shell cat VERSION)
	@docker push $(LOCAL_TAG):$(shell cat VERSION)

run: ## Run the (local) Docker image
	@docker run --rm -it $(LOCAL_TAG):$(shell cat VERSION) /bin/bash

ping: ## Test AWX connectivity and access
	@curl -s -H "Authorization: Bearer ${TOWER_OAUTH_TOKEN}" \
		"${TOWER_HOST}/api/v2/users/" | jq -r .

validate: ## Validate the pipeline
	@fly --target $(CONCOURSE_TARGET) validate-pipeline \
		--config pipeline.yml \
		--var TOWER_HOST=$(TOWER_HOST) \
		--var TOWER_OAUTH_TOKEN=$(TOWER_OAUTH_TOKEN) \
		--var TOWER_JOB_TEMPLATES=$(TOWER_JOB_TEMPLATES)

set: ## Set the pipeline
	@fly --target $(CONCOURSE_TARGET) set-pipeline \
		--config pipeline.yml \
		--pipeline my-pipeline --non-interactive \
		--var TOWER_HOST=$(TOWER_HOST) \
		--var TOWER_OAUTH_TOKEN=$(TOWER_OAUTH_TOKEN) \
		--var TOWER_JOB_TEMPLATES=$(TOWER_JOB_TEMPLATES)

unpause: ## Unpause the pipeline
	@fly --target $(CONCOURSE_TARGET) unpause-pipeline --pipeline my-pipeline

launch: ## Launch the pipeline
	@fly --target $(CONCOURSE_TARGET) trigger-job --job my-pipeline/awx-job

shipit: build push set launch ## Build, push, set and launch
	@echo shipit
