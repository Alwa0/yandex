# Candy deliveries
REST API server that is able to recruit couriers, take orders, assign orders to couriers, and count their ratings and earnings.
## Prerequirments:
Check first to see if you have the tools required already installed:

    $ python3 --version
    $ pip3 --version
You can install Python and pip easily with apt install, just run the following commands:

    $ sudo apt install python3
    $ sudo apt install python3-pip

Check if git is installed:

    $ git --version
Install git by running coommands:

    $ sudo apt install git-all
    
Install the latest version of PostgreSQL:

    $ sudo apt-get install postgresql

## Installation:
1. Clone git repository`git clone https://github.com/Alwa0/yandex`
2. Change current directory: `cd yandex`
3. Install all libraries `pip3 install -r requirments.txt`
4. Create local postgresql database and add all required information to `yandex_test/settings.py` (by default postgresql, where name, user and password are 'postgres' listen on port 5432):

        $ sudo -u postgres psql
        postgres=# \password postgres
## Running the project

1. Run `python3 manage.py migrate` to apply migrations
2. Run `python3 manage.py runserver` to run server locally or `python3 manage.py runserver 0.0.0.0:8000` globally

To run tests:

    $ python3 manage.py test
