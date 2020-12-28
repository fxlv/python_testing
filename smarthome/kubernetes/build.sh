#!/bin/bash

# this script expects there to be a .config file which should define 4 variables:
# * BUILDER="IP address or hostname of your builder box"
# * REGISTRY_PATH="PATH/URL of your Container registry"
# * MQTT_SERVER="IP or hostname of your MQTT server"
# * MQTT_TOPIC="The topic for your light bulb"
# * START_TIME="HH:MM"
# * END_TIME="HH:MM"

# source the config
. .config

# version is taken from colorize.py file
VERSION=$(cat ../colorize.py  | grep "__version__"| awk '{ print $3 }'| sed  's/"//g')
IMAGE_NAME="${REGISTRY_PATH}/colorize:${VERSION}"

echo "Configuration variables"
echo "BUILDER: $BUILDER"
echo "VERSION: $VERSION"
echo "REGISTRY_PATH: $REGISTRY_PATH"
echo "IMAGE_NAME: $IMAGE_NAME"
echo "START_TIME: $START_TIME"
echo "END_TIME: $END_TIME"
sleep 1
echo "Preparing YAML definition for configmap"
cp -v configmap_TEMPLATE.yaml "configmap_${VERSION}.yaml"
sed -I .backup -e "s#START_TIME#${START_TIME}#" -e "s#END_TIME#${END_TIME}#" -e "s#MQTT_SERVER#${MQTT_SERVER}#" -e "s#MQTT_TOPIC#${MQTT_TOPIC}#" "configmap_${VERSION}.yaml"

sleep 1
echo "Preparing YAML definition for the Deployment"
cp -v colorize_TEMPLATE.yaml "colorize_${VERSION}.yaml"
sed -I .backup -e "s#VERSION#${VERSION}#" -e "s#IMAGE_NAME#${IMAGE_NAME}#" "colorize_${VERSION}.yaml"

sleep 1
echo "Building the Docker image"

ssh $BUILDER "rm -rfv colorizebuild"
ssh $BUILDER "mkdir colorizebuild"
scp "Dockerfile" "$BUILDER:~/colorizebuild/"
ssh $BUILDER "cd colorizebuild; sudo docker build -t ${IMAGE_NAME} -f Dockerfile . --no-cache"

echo "Uploading the image to registry"
ssh $BUILDER "sudo docker push ${IMAGE_NAME}"

echo "You can now deploy Colorize to kubernetes"
echo
echo "kubectl apply -f configmap_${VERSION}.yaml"
echo "kubectl apply -f colorize_${VERSION}.yaml"
echo
