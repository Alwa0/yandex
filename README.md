# Candy delivieres
REST API server that is able to recruit couriers, take orders, assign orders to couriers, and count their ratings and earnings.
## Prerequirments:
1. git
2. python
3. pip
## Installation:
1. clone git repository`git clone https://github.com/Alwa0/yandex`
2. Install all libraries `pip install -r requirments.txt`
3. create local database and add all required information to `yandex_test/settings.py` (by default postgresql, where name, user and password are 'postgres' listen on port 5432)
4. Run `python manage.py migrate` to apply migrations
5. Run `python manage.py runserver` to run server locally or `python manage.py runserver 0.0.0.0:8000` globally
