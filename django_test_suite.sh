#!/bin/sh

# Copyright (c) 2020 Google LLC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -x pipefail

sudo apt-get update -y
sudo apt-get install -y libmemcached-dev

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

export DJANGO_TESTS_DIR="django_tests_dir"
mkdir -p $DJANGO_TESTS_DIR

pip3 install -r requirements.txt
pip3 install -e .
git clone https://github.com/django/django.git $DJANGO_TESTS_DIR/django

# Install dependencies for Django tests.
sudo apt-get update
sudo apt-get install -y libffi-dev libjpeg-dev zlib1g-devel

cd $DJANGO_TESTS_DIR/django && pip3 install -e . && pip3 install -r tests/requirements/py3.txt; cd ../../

create_settings() {
    cat << ! > "test_yugabyte.py"
DATABASES = {
   'default': {
       'ENGINE': 'django_yugabytedb',                                                                          
       'NAME': 'yugabyte',                                                                              
       'HOST': 'localhost',                                                                             
       'PORT': 5437,                                                                                    
       'USER': 'yugabyte'
   },
   'other': {
       'ENGINE': 'django_yugabytedb',                                                                            
       'NAME': 'other',                                                                                
       'HOST': 'localhost',                                                                               
       'PORT': 5437,                                                                                      
       'USER': 'yugabyte' 
   },
}
SECRET_KEY = 'django_tests_secret_key'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

USE_TZ = False
!
}

cd $DJANGO_TESTS_DIR/django/tests
create_settings

EXIT_STATUS=0
for DJANGO_TEST_APP in $DJANGO_TEST_APPS
do
   echo "==========================================================================================="
   echo $DJANGO_TEST_APP
   echo "==========================================================================================="
   python3 runtests.py --settings=test_yugabyte -v 3 $DJANGO_TEST_APP --noinput || EXIT_STATUS=$?
done
exit $EXIT_STATUS