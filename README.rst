Django backend for YugabyteDB
=============================

Prerequisites
-------------

* GCC
* Python 3.8 and above 

Need for Django Backend for YugabyteDB
---------------------------------------

YugabyteDB needs a separate backend for Django. This is because of mainly 2 reasons.

* Django tries to create Inet data types as primary keys in Django test suites. Since this is not supported, we map Inet types to varchar(15) and varchar(39) in the YB backend.  
* We also need it to support type change from int to BigInt and numeric(m,n) to double precision. This is required  for Django DB migrations. For now, the YB backend ignores these type changes.


Installing in Python Virtual Environment From Source
---------------------------------------------------------

Install the yb-django package in the python virtual environment. Right now, you have to use the source code:

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
            'ENGINE': 'yb_backend',
            'NAME': 'yugabyte',
            'HOST': 'localhost',
            'PORT': 5433,
            'USER': 'yugabyte'
        }
    }
