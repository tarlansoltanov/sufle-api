compose-main = docker-compose.yml

# Environment
ENV ?= dev

# Service
svc :=

up:
	@echo "Running containers"
ifeq ("$(ENV)", "dev")
	docker compose up -d
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml up -d
endif

down:
	@echo "Stopping and Deleting containers"
ifeq ("$(ENV)", "dev")
	docker compose down
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml down
endif

down-v:
	@echo "Stopping and Deleting containers with related volumes"
ifeq ("$(ENV)", "dev")
	docker compose down -v
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml down -v
endif

restart:
	@echo "Restarting containers"
ifeq ("$(ENV)", "dev")
	docker compose restart $(svc)
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml restart $(svc)
endif

stop:
	@echo "Stopping containers"
ifeq ("$(ENV)", "dev")
	docker compose stop $(svc)
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml stop $(svc)
endif

log:
	@echo "Showing logs"
ifeq ("$(ENV)", "dev")
	docker compose logs $(svc)
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml logs $(svc)
endif

build:
	@echo "Building image"
ifeq ("$(ENV)", "dev")
	docker compose build $(svc)
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml build $(svc)
endif

get-cert:
	@echo "Testing certificate"
	docker compose --env-file config/.env -f docker/docker-compose.cert.yml up
