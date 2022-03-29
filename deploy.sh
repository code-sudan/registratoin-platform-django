#!/bin/sh     
source ./venv/bin/activate
sudo git pull origin master
sudo pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
sudo service apache2 restart
