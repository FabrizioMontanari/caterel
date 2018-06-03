#!/bin/bash
set -e

# build latest version
source env/bin/activate
python build.py

# copy static files to s3
printf 'Synchronizing files to s3...'
aws s3 sync static s3://static.imartinisisposano.it --acl public-read
printf 'Done\n\n'

# deploy with zappa to lambda
printf 'Deploying backend to lambda...'
cd backend
zappa update ${1:-dev}
printf 'Done\n\n'

# clean up
cd -
deactivate
echo 'Deployment completed.'