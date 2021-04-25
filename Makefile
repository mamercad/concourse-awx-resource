QUAY_TAG := quay.io/mamercad/concourse-awx-resource
LOCAL_TAG := registry:5000/concourse-awx-resource
TOWER_HOST := ${TOWER_HOST}
TOWER_OAUTH_TOKEN := ${TOWER_OAUTH_TOKEN}
TOWER_JOB_TEMPLATES := ${TOWER_JOB_TEMPLATES}
CONCOURSE_TARGET := tutorial
CONCOURSE_URL := http://localhost:8080
VERSION := $(shell cat VERSION)

.PHONY: docker-build docker-push docker-run concourse-up \
		concourse-login pipeline-validate pipeline-set \
		pipeline-unpause shipit

docker-build:
	@docker build -t $(QUAY_TAG):$(VERSION) .
	@docker build -t $(LOCAL_TAG):$(VERSION) .

docker-push:
	@docker push $(QUAY_TAG):$(VERSION)
	@docker push $(LOCAL_TAG):$(VERSION)

docker-run:
	@docker run --rm -it $(LOCAL_TAG):$(VERSION) /bin/bash

concourse-up:
	@docker-compose up -d

concourse-login:
	@fly -t $(CONCOURSE_TARGET) login -c $(CONCOURSE_URL) -u test -p test

pipeline-validate:
	@fly --target $(CONCOURSE_TARGET) validate-pipeline \
		--config pipeline.yml \
		--var TOWER_HOST=$(TOWER_HOST) \
		--var TOWER_OAUTH_TOKEN=$(TOWER_OAUTH_TOKEN) \
		--var TOWER_JOB_TEMPLATES=$(TOWER_JOB_TEMPLATES)

pipeline-set:
	@fly --target $(CONCOURSE_TARGET) set-pipeline \
		--config pipeline.yml \
		--pipeline my-pipeline --non-interactive \
		--var TOWER_HOST=$(TOWER_HOST) \
		--var TOWER_OAUTH_TOKEN=$(TOWER_OAUTH_TOKEN) \
		--var TOWER_JOB_TEMPLATES=$(TOWER_JOB_TEMPLATES)

pipeline-unpause:
	@fly --target $(CONCOURSE_TARGET) unpause-pipeline --pipeline my-pipeline

pipeline-launch:
	@fly --target $(CONCOURSE_TARGET) trigger-job --job my-pipeline/awx-job

shipit: docker-build docker-push pipeline-set pipeline-launch
	@echo shipit
