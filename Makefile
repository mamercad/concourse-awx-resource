QUAY_TAG := quay.io/mamercad/concourse-awx-resource
LOCAL_TAG := registry:5000/concourse-awx-resource
TOWER_HOST := ${TOWER_HOST}
TOWER_OAUTH_TOKEN := ${TOWER_OAUTH_TOKEN}

.PHONY: docker-build docker-push docker-run concourse-up \
		concourse-login pipeline-validate pipeline-set \
		pipeline-unpause shipit

docker-build:
	@docker build -t $(QUAY_TAG) .
	@docker build -t $(LOCAL_TAG) .

docker-push:
	@docker push $(QUAY_TAG)
	@docker push $(LOCAL_TAG)

docker-run:
	@docker run --rm -it $(LOCAL_TAG) /bin/bash

concourse-up:
	@docker-compose up -d

concourse-login:
	@fly -t tutorial login -c http://localhost:8080 -u test -p test

pipeline-validate:
	@fly --target tutorial validate-pipeline \
		--config pipeline.yml --var TOWER_HOST=$(TOWER_HOST) \
		--var TOWER_OAUTH_TOKEN=$(TOWER_OAUTH_TOKEN)

pipeline-set:
	@fly --target tutorial set-pipeline --config pipeline.yml \
		--pipeline my-pipeline --non-interactive \
		--var TOWER_HOST=$(TOWER_HOST) \
		--var TOWER_OAUTH_TOKEN=$(TOWER_OAUTH_TOKEN)

pipeline-unpause:
	@fly --target tutorial unpause-pipeline --pipeline my-pipeline

pipeline-launch:
	@fly --target tutorial trigger-job --job my-pipeline/awx-workflow

shipit: docker-build docker-push pipeline-set pipeline-launch
	@echo shipit
