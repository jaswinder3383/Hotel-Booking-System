#!/bin/sh
# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"
# Apply database migrations
echo "Applying database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate
# Automatically create a superuser if it doesn't exist
echo "Creating superuser..."
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'password')"
# Start the Django development server
echo "Starting server..."
python3 manage.py runserver 0.0.0.0:8000





