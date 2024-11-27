.PHONY: help
help:
	@echo "Makefile targets:"
	@echo "  install                              - Install all dependencies using poetry"
	@echo "  run                                  - Run the application using poetry"
	@echo "  coverage                             - Run tests and show code coverage"
	@echo "  docker-up                            - Start the application and Redis using Docker Compose"
	@echo "  docker-down                          - Stop Docker Compose"
	@echo "  clean                                - Clean temporary files, docker data, and pytest cache"
	@echo "  poetry-export-requirements           - Export dependencies from poetry to requirements.txt"


.PHONY: install
install:
	@poetry install


.PHONY: poetry-export-requirements
poetry-export-requirements:
	@poetry export --format requirements.txt --output requirements.txt --without-hashes


.PHONY: run
run:
	@poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


.PHONY: coverage
coverage:
	@poetry run pytest --cov=app --cov-report=term-missing

.PHONY: docker-up
docker-up:
	docker compose up --build

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: clean
clean:
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@rm -rf .pytest_cache
	@docker compose down --volumes --remove-orphans --rmi local --timeout 0
