DATABASES = {
    'default': {
        'ENGINE': 'yb_backend',
        'NAME': 'yugabyte',
        'HOST': 'localhost',
        'PORT': 5433,
        'USER': 'yugabyte'
    },
    'other': {
        'ENGINE': 'yb_backend',
        'NAME': 'yugabyte',
        'HOST': 'localhost',
        'PORT': 5433,
        'USER': 'yugabyte'
    },
}
SECRET_KEY = 'yb_secret_key'
