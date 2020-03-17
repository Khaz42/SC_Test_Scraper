# SensCritique Test - Web Scraper

### PostgreSQL Setup
1. After installing PostgreSQL locally : add 'PostgreSQL/\<version>/bin to PATH.
2. To make sure the export to PATH worked, enter 'pg_config' in the terminal. It should not return "command not found".
3. Log into PostgreSQL using the "psql" command
4. Setting up the database for the app
```
CREATE DATABASE testscraper;
CREATE USER scraperuser WITH PASSWORD 'scraperuser';
ALTER ROLE scraperuser SET client_encoding TO 'utf8';
ALTER ROLE scraperuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE scraperuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE testscraperTO myprojectuser;
```
5. "\q" to quit psql

### Virtual Environment
1. Creating the virtual environment
```
python -m venv <env_name>
```
2. Activating the virtual environment
```
Linux :   source <env_name>/bin/activate
Windows : source <env_name>/Scripts/activate
```
3. Installing the required packages
```
pip install -r requirement.txt
```

### Launching the app
1. Make the migration from the Django models to the PostgreSQL database
```
python manage.py makemigrations
python manage.py migrate
```
2. (Optional) Creating a superuser, who can access the admin page
```
python manage.py createsuperuser
```
3. Starting the application
```
python manage.py runserver
```
4. Then go to http://localhost:8000/ to use the application, or to http://localhost:8000/admin to access the database directly.
