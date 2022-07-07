## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

#### Python and virtual environment (linux)

* Using python virtualenv as virtual environment
Install python virtualenv and activate the virtualenv

    ```shell
    $ pip install virtualenv
    Collecting virtualenv...
    $ virtualenv .venv
    created virtual environment...
    $ source .venv/bin/activate
    (.venv) $
    ```

### Installing
1. Installing python dependencies
    ```shell
    $ pip install -r requirements.txt
    ```

2. Create .env file, the example file format is provided in this repo, you can copy from that example and adjust it.
    ```shell
    $ cp .env.example .env
    -
    ```

3. Update database migrations to the latest version

    ```shell
    $ flask db upgrade head
    -
    ```

4. Running development server

    ```shell
    $ flask run
    -
    ```

### Database Migration
1. To create database migration, update/create file in :
    **/srv/models/{filename}.py**

2. Then create migration file by using following command :
    ```shell
    $ flask db migrate --rev-id {rev_id} -m {message}
    $ Generating /Users/marchandev/Backend/Okami/plnsc/hrms-api/migrations/versions/03_2022-03-11_readme.py ...  done
    ```

3. Migration file will created in :

   **/migrations/versions**

4. Update database migrations to the latest version

    ```shell
    $ flask db upgrade head
    -
    ```

### Project Structure
    .
    ├── ...
    ├── migrations              # Migrations parent folder
    │   └── versions            # Migrations versions
    ├── srv                     # Main projects structure
    │   ├── blueprints          # Flask blueprint, set path and regist here
    │   ├── controllers         # Controller base function for each feature
    │   ├── helpers             # Set global helper function here (loaders etc.)
    │   ├── models              # Models for our database's structure
    │   ├── resources           # Flask view function
    │   └── seeds               # Seeder data for our database
    └── ...


### Cron schedule
This is the necessary cron schedule to check every minute which email that needed to send in that time

    ```shell
    * * * * * cd /path/to/project/directory && .venv/bin/flask scheduler event_checker
    -
    ```
