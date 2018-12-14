call venv\scripts\activate.bat
echo from django.contrib.sites.models import Site; Site.objects.create(name='localhost', domain='127.0.0.1:8000') | python manage.py shell
pause