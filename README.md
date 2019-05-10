# STI dashboards

## Installation

* clone the repository

  ```shell
  git clone git@github.com:epfl-sti/sti_dashboards.git
  ```

* get into the repository

  ```shell
  cd sti_dashboards
  ```

* create a virtual environment and activate it

  ```shell
  virtualenv venv
  source ./venv/bin/activate
  ```

* Install the dependencies

  ```shell
  pip install -r requirements.txt
  ```

* Apply the migrations

  ```shell
  python manage.py migrate
  ```

* Collect the static files

  ```shell
  python manage.py collectstatic
  ```

* (dev) Run the local server

  ```shell
  python manage.py runserver
  ```
