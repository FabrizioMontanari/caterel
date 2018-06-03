#!/bin/bash
set -e

python -m http.server &
FLASK_APP=backend/martini.py FLASK_DEBUG=1 flask run