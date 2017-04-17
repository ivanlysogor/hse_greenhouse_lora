import paho.mqtt.client as mqtt
import json
import redis


import time
import sys
import pprint
import uuid

# ------ Import IBM libraries

try:
	import ibmiotf.application
	import ibmiotf.device
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device


def myAppEventCallback(event):
	print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

 
# ----- IBM Watson config

organization = "tulocj"
deviceType = "LORA"
deviceId = "LMT01"
appId = deviceId + "_receiver"
authMethod = "token"
authToken = "Rv8xQ4YVF*6V9nfRdQ"

# Initialize the application client.
try:
	appOptions = {"org": organization, "id": appId, "auth-method": authMethod, "auth-token": authToken}
	appCli = ibmiotf.application.Client(appOptions)
except Exception as e:
	print(str(e))


# Connect and configuration the application
# - subscribe to live data from the device we created, specifically to "greeting" events
# - use the myAppEventCallback method to process events

# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

def publish_callback(result, status):
    print "status.is_error", status.is_error()
    print "status.original_response", status.original_response
    pass
    # Handle PNPublishResult and PNStatus

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("devices/lora/#")

def myOnPublishCallback():
    print("Confirmed event received by IoTF\n")


# ------ MQTT Message parsing
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    #  ----  Debug received event
    print(msg.topic+" "+str(msg.payload))
    
    # ----- send to local Redis
    r.append(msg.topic,str(msg.payload)+'/')
    datajson=json.loads(str(msg.payload))
    print datajson['data']
    
    # -----  sent to remote_redis
    r.append(msg.topic,str(msg.payload)+'/')

    # ----- send to IBM Watson
    success = deviceCli.publishEvent("data", "json", datajson['data'], qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")

# ------ Redis local connect

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# ------ redis remote

config = {
    'host': 'iotRedis.redis.cache.windows.net',
    'port': 6379,
    'password': "i5hFZUx3D6GTMtA/UcI+P3HFf4O63I/HYbEEa/p/aJU="
}

r_remote = redis.StrictRedis(**config)


# ------ MQTT Connect

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
