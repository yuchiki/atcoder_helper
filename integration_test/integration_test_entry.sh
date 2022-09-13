set eux

IMAGE_TAG=atcoder_helper_integration_environment

docker build -f integration_test/Dockerfile -t $IMAGE_TAG .
docker run $IMAGE_TAG integration_test/integration_test.sh
