# HotZone---github: Quick Start Guide

This tutorial is use to test the Django server locally.

1. Get the git source code:
2. `git clone https://github.com/PCRedHot/HotZone---github.git` 

2. Go to the directory:

   `cd HotZone---github` 

3. Open pipenv shell by

    `pipenv shell`

4. Install dependencies:

   `pipenv install`

5. Go to Django Project Folder

   `cd hotzone1`

6. Migrate all model files to database

   `python manage.py migrate`

7. Create Superuser

   `python manage.py createsuperuser`

8. Start Server

   `python manage.py runserver`
