ReadMe
Django version: 1.8.0
Python version: 2.7.3
Omero server and web installation: 
https://docs.openmicroscopy.org/omero/5.4.3/sysadmins/unix/server-installation.html
Omero python packages: 
https://docs.openmicroscopy.org/omero/5.4.0/developers/Python.html

Packages you need to import in Django:
mysql in your laptop
(you need to change the user, password, port, host information in setting.py according to your mysql database)
packages in Django:
pip install mysqlclient
pip install captcha

run the following commands in terminal
python manage.py migrate
python manage.py makemigrations 
to migrate the project

run the project and visit localhost:8000/index to visit the main page.

You need to connect with Georgia Tech vpn to see the images
