#! /bin/bash
sh clean.sh
pip install -r requirements.txt
./manage.py makemigrations language answer chapter course document question users year
./manage.py migrate
./manage.py createsuperuser
./manage.py shell < data.py 
./manage.py runserver
