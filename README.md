# I Martini Si Sposano

## Installation

* create a virtualenv with `python==3.6.4` and `pip==9.0.1`
* activate the virtualenv
* run `pip install -r requirements.txt`

## Development

* all base files are in src and development should be done there
* to start a local server you can run `FLASK_APP=martini.py flask run`

## Deployment

* run `python deploy.py` in the root folder to copy/compile the files
* deploy the backend with `zappa update <stage>` (dev/prod)
* copy the content of the static folder to s3
