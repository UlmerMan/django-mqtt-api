import time

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view

import paho.mqtt.client as mqtt

import logging
logger = logging.getLogger('django')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

#    time.sleep(5)
 #   mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_disconnect = on_disconnect
try:
    mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
except Exception as e:
    pass

@api_view(['POST'])
def postData(request):
    mqttc.publish(request.data.get('topic'), request.data.get('message'))
    logger.debug(request.data)
    return Response('HTTP_200_OK')
    #else:
        #logger.debug(request.data)
        #return Response('HTTP_500_Internal_Server_Error')