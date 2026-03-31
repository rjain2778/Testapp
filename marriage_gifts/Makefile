.PHONY: help install dev start test clean build deploy

help:
	@echo "Marriage Gifts API - Makefile Commands"
	@echo ""
	@echo "Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run development server"
	@echo "  make start      - Start all services with docker-compose"
	@echo "  make stop       - Stop all services"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build docker image"
	@echo "  make deploy     - Deploy to production"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make db-up      - Start database only"
	@echo "  make db-down    - Stop database only"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

dev:
	@echo "Starting development server..."
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

start:
	@echo "Starting all services..."
	docker-compose up -d

stop:
	@echo "Stopping all services..."
	docker-compose down

test:
	@echo "Running tests..."
	pytest

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/
	docker-compose down -v

build:
	@echo "Building docker image..."
	docker-compose build

deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

lint:
	@echo "Running linter..."
	ruff check app/

format:
	@echo "Formatting code..."
	ruff format app/

db-up:
	@echo "Starting database..."
	docker-compose -f docker-compose.yml --file docker-compose.db.yml up -d postgres redis

db-down:
	@echo "Stopping database..."
	docker-compose -f docker-compose.yml --file docker-compose.db.yml down
