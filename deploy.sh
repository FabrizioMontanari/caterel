#!/bin/bash
set -e

# build latest version
source env/bin/activate
python build.py

# copy static files to s3
echo 'Synchronizing files to s3...'
aws s3 sync static s3://www.imartinisisposano.it/static
echo 'Done'

# deploy with zappa to lambda
echo 'Deploying backend to lambda...'
cd backend
zappa update ${1:-dev}
echo 'Done'

# clean up
cd - > /dev/null
deactivate
echo 'Deployment completed.'
