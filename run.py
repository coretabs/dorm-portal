import os
import platform

venv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv')
is_venv_exist = os.path.isdir(venv_path) & os.path.exists(venv_path)

print(venv_path)
print(platform.system())

command = r'python manage.py runserver'

if platform.system() == 'Windows':
    if not is_venv_exist:
        print('creating virtual environment...')
        os.system('virtualenv venv')

        print('installing requirements...')
        os.system(r'venv\scripts\pip install -r requirements.txt')

    run_script = fr'''call venv\scripts\activate.bat & {command} & pause'''

elif platform.system() == 'Linux':
    if not is_venv_exist:
        os.system('virtualenv venv')

        print('installing requirements...')
        os.system('venv/bin/pip3 install -r requirements.txt')

    run_script = f'sudo chmod +x ./venv/bin/activate && ./venv/bin/activate && {command}'

os.system(run_script)
