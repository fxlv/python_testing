## Config map
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: colorize
data:
  mqtt_server: "127.0.0.1"
  mqtt_topic: "zigbee2mqtt/YOUR_BULB_NAME_HERE/set"
```

