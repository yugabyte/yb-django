Django backend for YugabyteDB
=============================

Prerequisites
-------------

* GCC
* Python 3.8 and above 
* Psycopg2-yugabytedb (recommended)
* Django 3.2 or above

Need for Django Backend for YugabyteDB
---------------------------------------

YugabyteDB needs a separate backend for Django. This is because of mainly 3 reasons.

* Django tries to create Inet data types as primary keys in Django test suites. Since this is not supported, we map Inet types to varchar(15) and varchar(39) in the YB backend.  
* We also need it to support type change from int to BigInt and numeric(m,n) to double precision. This is required  for Django DB migrations. For now, the YB backend ignores these type changes.
* The Django PostgreSQL Backend does not support the Load Balance, even when used with YugabyteDB smart driver. 
  
Installing from Pypi
---------------------

Install the django-yugabytedb package with the command:

.. code-block:: console

    $ pip install django-yugabytedb


Installing in Python Virtual Environment From Source
---------------------------------------------------------

The django-yugabytedb package can also be installed from source:

.. code-block:: console

    $ git clone https://github.com/yugabyte/yb-django.git

    $ python -m pip install -r <repo_path>/yb-django/requirements.txt

    $ python -m pip install -e <repo_path>/yb-django/

Check if it is installed correctly:

.. code-block:: console

    $ pip list —local

Use the backend with your Application
-------------------------------------

Update the ``DATABASES`` setting in your Django project's settings to point to YB server using Django YB backend:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django_yugabytedb',
            'NAME': 'yugabyte',
            'HOST': 'localhost',
            'PORT': 5433,
            'USER': 'yugabyte',
        }
    }

To use Cluster Aware Load Balance:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django_yugabytedb',
            'NAME': 'yugabyte',
            'HOST': 'localhost',
            'PORT': 5433,
            'USER': 'yugabyte',
            'LOAD_BALANCE': 'True'
        }
    }

To use Topology Aware Load Balance:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django_yugabytedb',
            'NAME': 'yugabyte',
            'HOST': 'localhost',
            'PORT': 5433,
            'USER': 'yugabyte',
            'LOAD_BALANCE': 'True',
            'TOPOLOGY_KEYS': 'cloud1.region1.zone1'
        }
    }

Known bugs and issues
-----------------------

* The creation of indexes in YugabyteDB is a little slow.
* Since Inet is mapped to varchar in the backend, comparison between data in the inet column wth Inet type will fail.
* For YugabyteDB verions earlier than 2.9, the savepoint feature is not supported.
* Dropping of Primary keys are not supported
* Alter table Add column Unique is not yet supported.
* Backfilling of existing rows when new column is added with default value is not yet implemented in yugabytedb.
* Type change from int to BigInt and numeric(m,n) to double precision is not yet supported.
* ALTER INDEX not supported yet.