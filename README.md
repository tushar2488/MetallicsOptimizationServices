# REST API for a metallics optimization service.

# Technology used
  - Python 3.8.3
  - Django 3.1.2
  - Postgres 9.5.22

# Backend
  - Django==3.1.2
  - django-filter==2.4.0
  - django-rest-swagger==2.2.0
  - djangorestframework==3.12.1
  - psycopg2==2.8.6

# Database:
  - Default SQLite databases used.
  
# Backend steps to follow
Environment Setup:
  1. Create and setup Django Env.
      >> Create Project Dir : MetallicsOptimizationServices
      >> Open In CMD: C:\Users\...\MetallicsOptimizationServices
  2. Create Virtual Env(Python 3.8) : 
      >> python -m venv env
  3. Activate Virtual Env:
      >> env\scripts\activate
  4. Install Django & REST Framework in venv
      >> python -m pip install django
      >> python -m pip install djangorestframework
    
# Project & App:
  1.  >> django-admin startproject metallics_services_api .
  2.  >> python manage.py startapp metallics_api
  3.  >> python manage.py migrate

# Create superuser :
  >> python manage.py createsuperuser --username tushar.tajne --email xxxxxxxx@gmai.com

# Generate Auth Token For REST API:
  >> python manage.py drf_create_token tushar.tajne
  Note: if you foget token. Login to django admin dashboard to get token. 

# ###############################
# List Of Features and Modules Inclusded In this Project:
# ###############################

  - Create Modals : 1. Chemical Elements 2. Commodity 3. Chemical Composition
  - Add New Chemical Elements & Get/List all Chemical Elements
  - Add new commodity & Get/List all with chemical composition
  - Add new chemical composition & Get/List all chemical composition
  - Renmove chemical composition by (elemen_id,commodity_id)
  - Update commodity by id
  - Get Commodity by id

# Note : for detail output please ref output.txt