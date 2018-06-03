# I Martini Si Sposano

## Requirements

* Python 3.6.4
* Pip 9.0.1 (10+ won't work)
* AWS cli configured with access

## Installation

* Create a virtualenv called `env`
* Activate the virtualenv
* Run `$ pip install -r requirements.txt`

## Development

* All base files are in src and development should be done there
* Run `$ python build.py` in the root folder to compile and copy the files from the source directory
* Run `$ FLASK_APP=martini.py flask run` in the `backend` folder to start a local development server

## Deployment

* Ensure the virtualenv is present and all requirements are installed. Does not need to be active.
* Run `$ bash deploy.sh <dev|prod>` in the root folder to compile and deploy the new version. Defaults to `dev`
