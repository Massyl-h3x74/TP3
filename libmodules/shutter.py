#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Shutter module
#

# Import zone #############################################################################
import time
import json
import threading
import paho.mqtt.client as mqtt_client
import os
import sys
from libmodules.connection_interface import CommunicationModule

# MQTT CLIENT CONF #############################################################################
MQTT_SERVER="192.168.0.210"
MQTT_PORT=1883
MQTT_USER="azerty"
MQTT_PASSWD="azerty"
# Full MQTT_topic = MQTT_BASE + MQTT_TYPE
MQTT_BASE_TOPIC = "1R1/014"
MQTT_TYPE_TOPIC = "shutter"
MQTT_PUB = "/".join([MQTT_BASE_TOPIC, MQTT_TYPE_TOPIC])
MQTT_SUB = "/".join([MQTT_PUB, "command"])
# 0: (default) no ACK from server | 1: server will ack every message
MQTT_QOS=0
# First subscription to same topic (for tests)
#MQTT_SUB = MQTT_PUB
# ... then subscribe to <topic>/command to receive orders



# Functions #############################################################################


# Classes #############################################################################

class Shutter(CommunicationModule):

    # class attributes
    SHUTTER_POS_CLOSED  = 0
    SHUTTER_POS_OPEN    = 1
    SHUTTER_POS_UNKNOWN = 2

    SHUTTER_ACTION_CLOSE    = 0
    SHUTTER_ACTION_OPEN     = 1
    SHUTTER_ACTION_STOP     = 2
    SHUTTER_ACTION_IDLE     = 3
    SHUTTER_ACTION_UNKNOWN  = 4

    SHUTTER_TYPE_WIRED = 0
    SHUTTER_TYPE_WIRELESS = 1
    # Min. and max. values for shutter course time
    MIN_COURSE_TIME         = 5
    MAX_COURSE_TIME         = 60

    # attributes
    _status = SHUTTER_POS_UNKNOWN
    shutterType = SHUTTER_TYPE_WIRED
    courseTime  = 30;       # (seconds) max. time for shutter to get fully open / close

    _backend    = None      # current backends
    _upOutput   = None
    _downOutput = None
    _stopOutput = None

    _curCmd     = None
    _thread     = None      # thread to handle shutter's course
    _condition  = None      # threading condition

    def __init__(self, unitID,shutterType="wired", courseTime=30, io_backend=None, upOutput=None, downOutput=None, stopOutput=None, shutdown_event=None, *args, **kwargs):
        ''' Initialize object '''
        super().__init__(mqtt_topics={'shutter'},unitID=unitID)
        self.shutterType = shutterType
        self.courseTime = courseTime
        self._backend = io_backend
        self._upOutput = upOutput
        self._downOutput = downOutput
        self._stopOutput = stopOutput

    # The callback for a received message from the server.
    def on_message(client, userdata, msg):
        ''' process incoming message.
            WARNING: threaded environment! '''
        payload = json.loads(msg.payload.decode('utf-8'))
        if(payload['topic'] == MQTT_SUB):
            if(payload['value']=='UP'):
                log.debug('UP')
            elif(payload['value'] == 'DOWN'):
                log.debug('DOWN')
            else:
                 log.debug('UNDIFINED')

        log.debug(
            "Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))


# #############################################################################
#
# MAIN
#

def main():

    #TODO: implement simple tests of your module
    shutter_01 =  Shutter(unitID='ALL')




# Execution or import
if __name__ == "__main__":

    # Logging setup
    logging.basicConfig(format="[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s", stream=sys.stdout)
    log = logging.getLogger()

    print("\n[DBG] DEBUG mode activated ... ")
    log.setLevel(logging.DEBUG)
    #log.setLevel(logging.INFO)

    # Start executing
    main()


# The END - Jim Morrison 1943 - 1971
#sys.exit(0)

