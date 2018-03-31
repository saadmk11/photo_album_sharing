#  Photo Album Sharing Service

Django Project for Creating Photo Albums & Sharing Them with Others.

## Features:

1. User can create multiple photo album
2. User can share albums.
3. Auto Generate URL and password to view the album.
4. Album rating and comment system.
5. User Registration.


## Prerequisites

Be sure you have the following installed on your development machine:

+ Python >= 3.6.3
+ Git 
+ pip
+ Virtualenv (virtualenvwrapper is recommended)

## Requirements

+ Django==1.11.11
+ django-crispy-forms==1.7.2
+ passlib==1.7.1
+ Pillow==5.0.0

## Installation

To setup a local development environment:

Create a virtual environment in which to install Python pip packages. With [virtualenv](https://pypi.python.org/pypi/virtualenv),
```bash
virtualenv venv            # create a virtualenv
source venv/bin/activate   # activate the Python virtualenv 
```

or with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/),
```bash
mkvirtualenv -p python3 {{project_name}}   # create and activate environment
workon {{project_name}}   # reactivate existing environment
```

Clone Github Project,
```bash
git clone https://github.com/saadmk11/photo_album_sharing.git
cd photo_album_sharing
```

Install development dependencies,
```bash
pip install -r requirements.txt
```

Migrate Database,
```bash
python manage.py migrate
```

Run the web application locally,
```bash
python manage.py runserver # 127.0.0.1:8000
```

Create SuperUser,
```bash
python manage.py createsuperuser
```
