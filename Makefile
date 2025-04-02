# Variables
PYTHON = python3.10

# Ruff lint
lint:
	$(PYTHON) -m ruff check --fix

# Ruff format	
format:
	$(PYTHON) -m ruff format

# Pytest
test:
	$(PYTHON) -m pytest

# Run docker-compose
docker-up:
	docker-compose up -d

# Stop docker-compose
docker-down:
	docker-compose down