in settings.py you might need to change the database credetials to meet yours. Or you may chage the database code to use the default database.
here is the code to do that..

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}


Also create admin login using the command below

            python manage.py createsuperuser

Login into the admin panel and add the followiing into the categories table using using this order

            1. crop
            2.livestock
            3.other

make sure to follow that oder create crops first then livestock and finally create other
