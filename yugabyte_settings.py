DATABASES = {
    'default': {
        'ENGINE': 'django_yugabytedb',
        'NAME': 'yugabyte',
        'HOST': 'localhost',
        'PORT': 5433,
        'USER': 'yugabyte'
    },
    'other': {
        'ENGINE': 'django_yugabytedb',
        'NAME': 'yugabyte',
        'HOST': 'localhost',
        'PORT': 5433,
        'USER': 'yugabyte'
    },
}
SECRET_KEY = 'yb_secret_key'
