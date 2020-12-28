# Deploying

This script can run as a command line script.
However I am deploying it on my Kubernetes cluster and therefore 
that is the supported means of deploying and operating it.

## Configuration

The script discovers configuration from environment variables.
There are required and optional variables.

### Required variables

* *MQTT_SERVER* as the name implies, this is the IP or hostname of your MQTT server.
* *MQTT_TOPIC* - this is the topic for your light bulb, for example `zigbee2mqtt/colorbulb/set`

### Optional variables

* *START_TIME* - start time in HH:MM format
* *END_TIME*  - end time in HH:MM format

## Containerisation

`kubernetes` directory contains some useful code to help deploy this script on kubernetes.

`build.sh` is a script I use to build a Docker image as well as the kubernetes definitions.
Since my Kube cluster runs on Raspberry Pis, then the build has to happen on my Rpi builder as well.

