set eux

IMAGE_TAG=atcoder_helper_integration_environment

docker build -f integration_test/Dockerfile -t $IMAGE_TAG .
docker run \
    --env ATCODER_HELPER_NAME=${ATCODER_HELPER_NAME:-""} \
    --env ATCODER_HELPER_PASSWORD=${ATCODER_HELPER_PASSWORD:-""} \
    $IMAGE_TAG \
    integration_test/integration_test.sh
