#!/bin/bash -e

# This script will start a new container mounting the repository and run the type checking, linting,
# code formatter and import formatter.
#
# 1. Runs black to not give you any more hope in life
# 2. Lints code to ensure code follows flake8 rules
# 3. Static type checking via mypy
# 4. Sorts imports via isort

CI_DIR=$(dirname $0)
SCRIPT_DIR=$(dirname $CI_DIR)
PROJECT_ROOT=${PWD}
PROJECT_NAME=bird_image_classification_mva
IN_CONTAINER_PROJECT_FOLDER=/deploy
JENKINS=${@: -1}


echo "Starting the container"
docker run -di --name $PROJECT_NAME-format -v $PROJECT_ROOT:$IN_CONTAINER_PROJECT_FOLDER registry.dathena.io/bird_image_classification_mva-$USER /bin/bash
echo "Container started"

CONTAINER_ID=$(docker ps -aq -f name=$PROJECT_NAME-format)

function cleanup {
    echo "Removing pycache files"
    docker start $CONTAINER_ID
    docker exec $CONTAINER_ID bash -c "find $IN_CONTAINER_PROJECT_FOLDER | grep -E \"(__pycache__|\.pyc|\.pytest_cache|\.pyo\$)\" | xargs rm -rf"
    docker stop $CONTAINER_ID
    docker rm $CONTAINER_ID
}

trap cleanup EXIT

# static type check
echo "Running type check..."
docker exec $CONTAINER_ID mypy --ignore-missing-imports --disallow-untyped-defs $IN_CONTAINER_PROJECT_FOLDER || exit 1
echo "Static type check passed"

# lint
echo "Running linter..."
docker exec $CONTAINER_ID flake8 --max-line-length=140 $IN_CONTAINER_PROJECT_FOLDER

# If the formatting actually changes files AND we are running this in jenkins,
# exit as soon as we have a wrong status code
exit_status=$?
if [ $exit_status -eq 1 ] && [[ $JENKINS == "true" ]];then
    echo "The code doesnt pass the linter (flake8)"
    exit 1
fi
echo "Linting passed"

# black formatting
echo "Running code formatter..."
docker exec -t $CONTAINER_ID bash -c "black --line-length 140 --skip-string-normalization $IN_CONTAINER_PROJECT_FOLDER" >&1 | tee /tmp/output_log.txt
# After saving the output to a file, grep the file for errors (this was the only way to save the exit status)
grep -q "reformatted" /tmp/output_log.txt

# If the formatting actually changes files AND we are running this in jenkins,
# exit as soon as we have a wrong status code
exit_status=$?
if [ $exit_status -eq 0 ] && [[ $JENKINS == "true" ]];then
    echo "Code was NOT formatted"
    exit 1
fi
echo "Code formatted"

# isort
echo "Running isort..."
docker exec $CONTAINER_ID isort \
  --atomic \
  --recursive \
  --project=$PROJECT_NAME \
  --section-default=THIRDPARTY \
  --multi-line=3 \
  --force-grid-wrap=0 \
  --combine-as \
  --line-width=140 \
  --trailing-comma \
  --apply \
  $IN_CONTAINER_PROJECT_FOLDER >&1 | tee /tmp/output_log.txt
# After saving the output to a file, grep the file for errors (this was the only way to save the exit status)
grep -q "Fixing" /tmp/output_log.txt

# If the formatting actually changes files AND we are running this in jenkins,
# exit as soon as we have a wrong status code
exit_status=$?
if [ $exit_status -eq 0 ] && [[ $JENKINS == "true" ]];then
    echo "Code imports were NOT ordered"
    exit 1
fi
echo "Sorted imports"

# static type check after formatting just to be sure
echo "Running type check..."
docker exec $CONTAINER_ID mypy --ignore-missing-imports --disallow-untyped-defs $IN_CONTAINER_PROJECT_FOLDER || exit 1
echo "Type check passed"

# lint
echo "Running linter..."
docker exec $CONTAINER_ID flake8 --max-line-length=140 $IN_CONTAINER_PROJECT_FOLDER || exit 1

# If the formatting actually changes files AND we are running this in jenkins,
# exit as soon as we have a wrong status code
exit_status=$?
if [ $exit_status -eq 1 ] && [[ $JENKINS == "true" ]];then
    echo "The code doesnt pass the linter (flake8)"
    exit 1
fi
echo "Linting passed"
