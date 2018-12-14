call venv\scripts\activate.bat
echo from api.engine.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin') | python manage.py shell
pause