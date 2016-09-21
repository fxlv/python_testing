#!/usr/bin/env python
#
# Send MARK messages to Syslog facilities
#
import logging
import logging.handlers

facilities = ["kern", "cron", "auth", "authpriv", "user", "daemon", "local0"]

marker = logging.getLogger('LogMarker')
marker.setLevel(logging.DEBUG)

for facility in facilities:
    handler = logging.handlers.SysLogHandler(address = '/dev/log', facility=facility)
    marker.addHandler(handler)
    marker.debug('-- MARK --')
