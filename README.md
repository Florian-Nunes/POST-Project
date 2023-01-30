# Cmdb Manager

## Presentation

On this project you will find the work that I realized during my internship period.

This project contains **2 folders** which represent the 2 following parts:

**- Infratool (django project for display)**

**- ETL (Python script for automation)**


--------------------------------------------------------------------------------
# Infratool

## Presentation :

* I/ Introduction
* II/ Setup
* III/ Structure
* IV/ Queries and responses
* V/ Models
* VI/ Ressources

--------------------------------------------------------------------------------

## I/ Introduction :

* Django is a Python-based framework for the Web that encourages fast, clean development with a pragmatic design
* Django allows you to build web applications quickly and with minimal code


--------------------------------------------------------------------------------


## II/ Setup :

### Introduction to virtualenv


    !shell
    $ virtualenv env  # create the environment
    (env) $ source env/bin/activate  # starts the virtual environment python
    (env) $ deactivate  # deactivate the virtual environment
    $ python --version // python3 --version  # to know the version of python


It is possible to create several different environments.

You should always **create the environment before starting the django project**.

Always **make sure** that it is __activated__.

### Creation and activation of *virtualenv*

    !console
    $ virtualenv envinfratool
    $ source envinfratool/bin/activate

### Django installation

    !console
    (venv) $ pip install django

### Creation of the project

    !console
    (venv) $ django-admin startproject projetinfratool

### Starting the development server

    !console
    (venv) $ cd projetinfratool
    (venv) $ python manage.py runserver


To make sure this works, we have this message in the terminal:

![Linux Terminal](img/terminal.jpg)

--------------------------------------------------------------------------------

## III/ Structure d'un projet Django

    !console
    └── projetinfratool
        ├── projetinfratool
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── asgi.py
        │   ├── urls.py
        │   └── wsgi.py
        └── manage.py

* ``projetinfratool`` : project container (the name is not important)
* ``projetinfratool/manage.py`` : command line utility allowing various actions on the project
* ``projetinfratool/projetinfratool`` : the actual Python package of the project
* ``projetinfratool/projetinfratool/settings.py`` : settings and configuration of the project
* ``projetinfratool/projetinfratool/asgi.py`` : ASGI config for projetinfratool
* ``projetinfratool/projetinfratool/urls.py`` : declaration of project URLs
* ``projetinfratool/libprojetinfratoolrary/wsgi.py`` : entry point for deploying the project with WSGI

### Projet vs. Application

It is important to differentiate between the notion of **project** and **application**.

### An application

> An application is a web application that does something - for example a blog system, a public database or a survey application

### A project

> A project is a set of settings and applications for a particular website.

### Projets and applications

> A project can contain several applications. An application can be included in several projects.

<cite> — docs.djangoproject.com</cite>

### A project is a composition of applications

* The project can be split into different apps
* The same app can be reused in several projects
* Django provides apps by default, for example to manage authentication
* Many other apps are made available by the community (installation via `pip`)
* A typical django project combines Django apps, community apps, and one or more 
community, and finally one or more project-specific apps
* These are python modules
* The `manage.py startapp` command automatically creates an app template in a new
directory.
* Apps are to be declared in the settings ( `INSTALLED_APPS = [...]` ) 


### Creating an application

    !console
    $ ./manage.py startapp ETL

### The application created

    !console
      ├── ETL/
      │   ├── __init__.py
      │   ├── admin.py
      |   ├── apps.py
      │   ├── migrations/__init__.py
      │   ├── models.py
      │   ├── tests.py
      │   ├── views.py

* ``models.py`` : declaration of the application models
* ``views.py`` : writing the views of the application
* ``admin.py`` : application performance in the administration interface
* ``tests.py`` : For test
* ``migrations``: successive changes to the database schema

**Activate the application !!! : **

### Declaration of the application in *settings*

    !python
    # settings.py
    INSTALLED_APPS = (
      'django.contrib.admin',
      ...
      'ETL',
    )

--------------------------------------------------------------------------------

## IV/ Queries and responses

### DB configuration

Django propose une configuration par défaut pour une base SQL (cf : ``settings.py``).

Voici un exemple de configuration pour une base SQL :

    !python
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbetl',
        'USER': 'infra',
        'PASSWORD': 'infratool',
        'HOST': 'localhost'
      }
    }

### Creating the initial structure of the database

    !console
    $ ./manage.py migrate

--------------------------------------------------------------------------------

## v/ The Models


### Models declaration

    !python
    # models.py
    from django.db import models

    class ecs(models.Model):
        InstanceName =  models.CharField(max_length=255)
        HostName = models.CharField(max_length=255)
        PrimaryIpAddress = models.CharField(max_length=255)
        OSName = models.CharField(max_length=255)
        InstanceTypeFamily = models.CharField(max_length=255)
        Cpu = models.IntegerField()
        Memory = models.IntegerField()
        Status = models.CharField(max_length=255)
        InstanceBandwidthRx = models.IntegerField()
        VSwitchID = models.CharField(max_length=255)
        SecurityGroupId = models.TextField()
        Lastseen = models.DateTimeField()

        def __str__(self):
            return ecs.InstanceName


Adding the ``Meta'' class to a model allows you to declare *metadata options* on the model. Example:

    !python
    class Book(models.Model):
        ...

        class Meta:
            db_table = 'ecs'
            verbose_name = 'Ecs'
            verbose_name_plural = 'Ecs'

### The Migration

**Very Important**

* Django allows models to evolve without deleting data by generating "diffs" called migrations which it then applies to the database
* It compares the last of the existing migrations to the models declared in python (no matter what is in the database)
* Then it converts to SQL and applies all migrations that have not already been done (the list of migrations already done is stored in the database)
* These migrations are numbered and stored in the apps in the subdirectory `migrations/`. It is advisable to register migrations with the code

### Creation of a migration 

    !console
    (venv) $ ./manage.py makemigrations

### Implementation of the migration

    !console
    (venv) $ ./manage.py migrate

### Reporting in the administration interface


    !python
    # admin.py
    from django.contrib import admin
    from books.models import ecs

    admin.site.register(ecs)
    class AdminEcsInfo(admin.ModelAdmin):
    list_display = ('InstanceName', 'HostName', 'PrimaryIpAddress', 'OSName', 'InstanceTypeFamily', 'Cpu', 'Memory', 'Status', 'InstanceBandwidthRx', 'VSwitchID', 'SecurityGroupId', 'Lastseen')
    
The administration interface is the automatic "back-office" of Django that 
lists the instances and by introspection of the models, creates the corresponding 
creation/modification forms.

It is customizable and allows to modify :

* filters and order of the lists
* the display of the lists
* forms and field order
* add mass actions to the lists


--------------------------------------------------------------------------------

## VI : Ressources :

### Environnement :

* Django 1.11+
* Python : 3.x
* Base de données : SQLite, PostgreSQL, MySQL

### KISS (*Keep It Simple, Stupid*)

> Simplicity should be a key goal in design and unnecessary complexity should be avoided.
### DRY (*Don't Repeat Yourself*)

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

### Architecture MVC, ou plutôt MTV

Django's architecture is based on the MVC (*Model, View, Controller*) or rather MTV (*Model, Template, View*) principle:

* **Model** : Models are written in Python and Django provides a full ORM (*Django ORM*) to access the database
* Template**: Django has its own template engine (*Django Template Engine*)
* **View** : Django views can be simple Python functions returning HTTP responses or they can be based on classes

The **controller** function is managed by the *URL dispatcher* which allows to map URLs as regular expressions to views.

--------------------------------------------------------------------------------
## ETL





--------------------------------------------------------------------------------
- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.ptech.lu/bes/infra/tools/cmdb-manager.git
git branch -M master
git push -uf origin master
```
