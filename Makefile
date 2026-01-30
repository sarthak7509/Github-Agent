# Variables
COMPOSE = docker compose

.PHONY: build up down restart logs clean

# Build or rebuild services
build:
	$(COMPOSE) build

# Start the services in detached mode
up:
	$(COMPOSE) up -d

# Stop the services
down:
	$(COMPOSE) down

# Restart the services
restart:
	$(COMPOSE) down && $(COMPOSE) up -d

# View real-time logs
logs:
	$(COMPOSE) logs -f

# Remove containers and volumes (wipes Redis data)
clean:
	$(COMPOSE) down -v
