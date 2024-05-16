# Portfolio App

# Installation
    (linux)
    git clone https://github.com/VPeron/flask_portfolio
    cd flask_portfolio
    activate virtualenvironment
    pip install -r requirements.txt
    sh setupdb.sh

# Usage

    python run.py

    http://127.0.0.1:5000/?



# GENERAL TODO:

    - tests
    - logger
    - deploy to linode (see https://www.youtube.com/watch?v=goToXTC96Co and https://www.linode.com/docs/guides/flask-and-gunicorn-on-ubuntu/)
    - create new v env => service_management_env is in use (needs to have its own venv)
    - pydantic for input validation?


# password strength checker app

### Checks the strength of the input string as for password usage.

# TODO:

    - generate random password section
    - improve UI/UX?

# hash calculator app

### Hashes the input string given the selected hashing algorythm.

# TODO:
- add more hash types
- compare hashe functionality
- improve UI/UX?
