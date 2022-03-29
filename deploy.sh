#!/bin/sh     
source ./venv/bin/activate
sudo git pull origin master
cat requirements.txt | xargs -n 1 pip install
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
sudo service apache2 restart