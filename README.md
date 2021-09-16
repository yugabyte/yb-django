# Django backend for YugabyteDB

## Prerequisites
* GCC
* Python 3.8 and above 

## Installing in Python Virtual Environment

Install the yb-django package in the python virtual environment. Right now, you have to use the source code.

```
git clone https://github.com/yugabyte/yb-django.git

python -m pip install -r <repo_path>/yb-django/requirements.txt

python -m pip install -e <repo_path>/yb-django/
```

Check if it is installed correctly 

```
pip list —local
```

Update the DATABASES section in in your Django application's settings.py to point to YB server using Django YB backend.

```
DATABASES = {
  'default': {
    'ENGINE': 'yb_backend',
    'NAME': 'yugabyte',
    'HOST': 'localhost',
    'PORT': 5433,
    'USER': 'yugabyte'
  }
}
```
