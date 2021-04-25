.PHONY: all

.DEFAULT_GOAL: help

help: ## Shows this help
	@fgrep -h "##" $(MAKEFILE_LIST) | \
		fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

status: ## Shows Concourse status
	@docker-compose ps

up: ## Spins up Concourse in Docker compose
	@docker-compose up -d

login: ## Set the fly Concourse target
	@fly --target $(CONCOURSE_TARGET) login \
		--concourse-url=$(CONCOURSE_EXTERNAL_URL) \
		--username=$(CONCOURSE_MAIN_TEAM_LOCAL_USER) \
		--password=$(CONCOURSE_MAIN_TEAM_LOCAL_PASS)

forget: ## Delete the fly Concourse target
	@fly delete-target --target $(CONCOURSE_TARGET)

down: ## Spins down Concourse
	@docker-compose stop

nuke: ## Nukes Concourse from Docker compose
	@docker-compose rm -f

crypto: ## Generates Docker registry crypto
	@openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 \
		-subj "/C=$(REGISTRY_COUNTRY)/ST=$(REGISTRY_STATE)/L=$(REGISTRY_LOCALITY)/O=$(REGISTRY_ORGANIZATION)/CN=$(REGISTRY_CANONICAL_NAME)" \
		-keyout registry.key -out registry.crt
