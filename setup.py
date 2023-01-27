from setuptools import find_packages, setup

import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 8)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of Django requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install django

This will install the latest version of Django which works on your
version of Python. If you can't upgrade your pip (or Python), request
an older version of Django:

    $ python -m pip install "django<2"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Framework :: Django :: 3.2
Framework :: Django :: 4.0
Intended Audience :: Developers
Operating System :: OS Independent
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Dynamic Content
Topic :: Internet :: WWW/HTTP :: WSGI
Topic :: Software Development :: Libraries :: Application Frameworks
Topic :: Software Development :: Libraries :: Python Modules
"""
try:
    f = open("README.rst")
    readme = f.read()
    f.close()
except Exception:
    print("failed to read readme: ignoring...")
    readme = __doc__
setup(name="django-yugabytedb",
version = "4.0.0.post1",
url = 'https://www.yugabyte.com/',
author = 'Yugabyte',
author_email = 'hbhanawat@yugabyte.com',
maintainer="Sfurti Sarah",
maintainer_email="ssarah@yugabyte.com",
description=readme.split("\n")[0],
long_description="\n".join(readme.split("\n")[2:]).lstrip(),
license = 'Apache',
classifiers =[x for x in classifiers.split("\n") if x],
project_urls ={
        'Documentation' : 'https://docs.yugabyte.com/',
        'Code': 'https://github.com/yugabyte/yb-django'
        }   
)
