echo "running server"
PORT=${PORT:-8000}
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn university.wsgi:application --bind 0.0.0.0:$PORT
python manage.py runserver