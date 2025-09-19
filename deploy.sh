#!/bin/bash

echo "🚀 Deploying Document AI Assistant..."

# Pull latest code
git pull origin main

# Build Docker image
docker-compose build

# Run migrations
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate

# Collect static files
docker-compose run --rm web python manage.py collectstatic --noinput

# Start services
docker-compose up -d

echo "✅ Deployment completed!"
echo "🌐 Application available at http://localhost:8000"