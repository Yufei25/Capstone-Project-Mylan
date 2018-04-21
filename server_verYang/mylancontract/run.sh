#!/bin/sh
sudo pip install --upgrade pip
virtualenv -p python venv
source venv/bin/activate
pip freeze > requirements.txt
pip install -r requirements.txt

python manage.py runserver 0:7000

