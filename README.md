# Stagings application

Test application for Django framework.

## Requirements

* PostgreSQL any version
* pip
* Python >= 2.7

## Installation


1. Install required packages to run the application: ` pip install -r requirements.txt`
2. Open `final/settings.py` and configure database settings in a `Dev` class. In general changing a `USERNAME` and a `PASSWORD` is enough
3. Create database: `createdb final`. `final` is a database name, you could change it on step 2
4. Create database schema for the application and populate the database with fixtures: `python manage.py syncdb`
5. Run application: `python manage.py syncdb`
6. Open browser: `open http://localhost:8000`

If you want to test user reqistration run a mailserver to receive emails for user activation instructions. With default settings the application will send the emails to a port `25`. The simplest way to run mailserver locally is to use this command:
`python -m smtpd -n -c DebuggingServer localhost:1025`. Now the mailserver listens to incoming emails for `1025/25` port.

Correctly installed application concains the following registered users in the system:

1. Superuser: admin/123
2. Client: client/123
3. Courier: courier/123

## Heroku

This application has already [deployed on Heroku](http://agile-atoll-1564.herokuapp.com).
