# Competitive Wikipedia Speedrunning

This repository holds the code for [wikispeedruns.com](https://wikispeedruns.com).

## 1. Prerequisites

- Python 3.7 or greater
- MySQL Server 8 [Download here](https://dev.mysql.com/downloads/)

## 2. Python Setup

#### Setup Virtual Environment (optional)
We recommend creating a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html)
for running the server.
```
python -m venv env
```

For Windows Powershell:
```
./env/Scripts/Activate.ps1
```

For Linux
```
source env/bin/activate
```

#### Install Requirements
Then install the requirements (with your virtual environment activated)
```
pip install -r requirements.txt
```

## 3. App Setup
There are a number of scripts to help setup the web app in [scripts](scripts).

Once the MySQL server is running, you will need to create an account. By
default we assume an account `user` with no password (see
[`default.json`](config/default.json)). If you wish to use a different MySQL
setup, you can create `prod.json` with the relevant MySQL fields in
[`config`](config) which will override `default.json`.

Then create the database and tables using the provided script.
```
cd scripts
python create_db.py
```

There is also an interactive script (with instructions in the scripts) which
can be used to set up a local admin account. Through the admin account, 
prompts can be managed through `/manage`.
```
cd scripts
python create_admin_account.py
```

(Optional) Finally, there is also a script to populate the database with data
for local development
```
cd scripts
python populate_db.py
```
## 4. Running

#### (Optional) Set environment variables for development
Set the environment variable `FLASK_ENV` in whaterver command prompt you use plan to use
for running the flask server. This will allow the local instance to reload automatically
when files are changed.

For example, in Linux
```
export FLASK_ENV="development"
```

Or in Windows Powershell
```
$env:FLASK_ENV="development"
```

#### Start the server
From the top level directory
```
flask run
```

## 5. Testing Locally

In order to run the [tests](test) locally, you need to create another account in MYSQL
with username `testuser` and password `testpassword`. Our tests are configured to run
against this account by default.

Then, simply run pytest from the `test` directory.
```
cd test
pytest
```

Note that these tests are also run in Docker upon making a PR using Github workflows.
In the future we may setup docker to run tests as well.


## 6. In-depth Setup for Testing (e.g. for STAD class)
First, ensure that you meet the prerequisites and have MySQL installed.

#### Database setup
Start the MySQL server in a terminal window. This can be achieved with the command
`mysql -u root -p`. On my machine (macOS 11), command `mysql` was not recognized. 
This can be remedied by running the command `/usr/local/mysql/bin/mysql -u root -p`.
Login with your root password.

Now, you need to create two users:
```
CREATE USER 'user'@'localhost';
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpassword';
```

Grant both users the necessary privileges. This can be achieved with:
```
GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'testuser'@'localhost';
```

Ensure that the MySQL server is running somewhere in the background when you are 
testing or running the app.

#### App setup
Install requirements (this is also done in the virtual environment, but I had to 
do it here as well to fix a weird import error):
`pip install -r requirements.txt` and 
`pip install coverage`

```
pip install -r requirements.txt
pip install coverage
pip install seleniumbase
pip install locust
pip3 install -U selenium
pip3 install webdriver-manager
```

Setup virtual environment:
```
python3 -m venv venv
source env/bin/activate
```

Install requirements in virtual environment just to be sure:
`pip install -r requirements.txt`, `pip install coverage`, `pip install seleniumbase`, `pip install locust`
```
pip install -r requirements.txt
pip install coverage
pip install seleniumbase
pip install locust
pip3 install -U selenium
pip3 install webdriver-manager
```

If not working later on: try installing this as well::
```
sbase install chromedriver latest
```

Create database:
```
cd scripts
python create_db.py
```

Populate database:
```
cd scripts
python populate_db.py
```

#### Running App
```
export FLASK_ENV="development"
flask run
```

#### Running Tests
```
export FLASK_ENV="development"
cd test
pytest
```

#### Obtaining Coverage
```
cd test
coverage run --branch -m pytest
coverage html
```
Now, check index.html in /test/htmlcov to view coverage analysis.

#### Run locust
```
cd test
locust
```
Runs locally on port 8089.



