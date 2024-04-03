#!/bin/bash

# ****************************
# *** Run Functional tests ***
# ****************************

HOST_URL=$1
echo $HOST_URL

# *** Test #1: Check the simple API call
responseCode=$(curl -s -o /dev/null -I -w "%{http_code}"  ${HOST_URL})
if [[ ${responseCode} != 200 ]]; then
    echo "Response code: $responseCode"
    echo "*** MLFlow Proxy API is not running"
    exit 1
fi

# *** Test #2: Check the experiments, models and runs API routers
responseCode=$(curl -s -o /dev/null -I -w "%{http_code}"  ${HOST_URL}/models)
if [[ ${responseCode} != 200 ]]; then
    echo "Response code: $responseCode"
    echo "*** Models API was not found"
    exit 1
fi

responseCode=$(curl -s -o /dev/null -I -w "%{http_code}"  ${HOST_URL}/experiments)
if [[ ${responseCode} != 200 ]]; then
    echo "Response code: $responseCode"
    echo "*** Experiments API was not found"
    exit 1
fi

responseCode=$(curl -s -o /dev/null -I -w "%{http_code}"  ${HOST_URL}/runs)
if [[ ${responseCode} != 200 ]]; then
    echo "Response code: $responseCode"
    echo "*** Runs API was not found"
    exit 1
fi

# *** Test #3: Check the dummy POST API
INPUT_DATA='{"disease": "AML", "description": "Jenkins Pipeline", "trained": "false"}'
MODEL_FILE_PATH='res/model.pk'
responseCode=$(curl -s -o /dev/null -I -w "%{http_code}"  -XPOST -H "Content-type:multipart/form-data" -d "${INPUT_DATA}" -F "${MODEL_FILE_PATH}"  ${HOST_URL}/models/upload/jenkins-func-test)
if [[ ${responseCode} != 201 ]]; then
    echo "*** Model upload POST API is not working properly"
    exit 1
fi

echo "*** Functional tests were successful ***"