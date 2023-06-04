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

up-build:
	@echo "Building images and Running containers"
ifeq ("$(ENV)", "dev")
	docker compose up -d --build
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml up -d --build
endif

up-wd:
	@echo "Running containers without daemon"
ifeq ("$(ENV)", "dev")
	docker compose up
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml up
endif

up-wd-build:
	@echo "Building images and Running containers without daemon"
ifeq ("$(ENV)", "dev")
	docker compose up --build
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml up --build
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
	@echo "Getting SSL certificate"
	docker compose --env-file config/.env -f docker/docker-compose.cert.yml up

# Django commands

createsuperuser:
	@echo "Django: Create Super User"
ifeq ("$(ENV)", "dev")
	docker compose exec web python manage.py createsuperuser
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml exec web python manage.py createsuperuser
endif

makemigrations:
	@echo "Django: Make Migrations"
ifeq ("$(ENV)", "dev")
	docker compose exec web python manage.py makemigrations
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml exec web python manage.py makemigrations
endif

migrate:
	@echo "Django: Migrate"
ifeq ("$(ENV)", "dev")
	docker compose exec web python manage.py migrate
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml exec web python manage.py migrate
endif

shell:
	@echo "Django: Shell"
ifeq ("$(ENV)", "dev")
	docker compose exec web python manage.py shell
else
	docker compose -f $(compose-main) -f docker/docker-compose.$(ENV).yml exec web python manage.py shell
endif