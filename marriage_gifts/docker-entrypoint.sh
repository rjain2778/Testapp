#!/bin/bash

# Wait for dependencies to be ready
echo "Waiting for Redis to be ready..."
until nc -z redis 6379; do
  sleep 1
done
echo "Redis is ready!"

echo "Waiting for PostgreSQL to be ready..."
until nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run application
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
