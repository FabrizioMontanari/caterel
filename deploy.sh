#!/bin/bash
set -e

# build latest version
source env/bin/activate
python build.py

# env check
stage=${1:-dev}
if [ "$stage" == "dev" ]; then acl="public-read"; else acl="private"; fi

# copy static files to s3
echo 'Synchronizing files to s3...'
aws s3 sync static "s3://www.imartinisisposano.it/static/${stage}" --acl=${acl}
echo 'Done'

# deploy with zappa to lambda
echo 'Deploying backend to lambda...'
cd backend
zappa update ${stage}
echo 'Done'

# clean up
cd - > /dev/null
deactivate
echo 'Deployment completed.'
