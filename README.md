in settings.py you might need to change the database credetials to meet yours. Or you may chage the database code to use the default database.
here is the code to do that..

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}
