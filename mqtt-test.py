import paho.mqtt.client as mqtt
import json
import redis
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

 
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-a2885d3a-222d-11e7-b284-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-aa6a2b58-13a0-4b05-abce-20cf4cc4f251"
pnconfig.ssl = False
 
pubnub = PubNub(pnconfig)

# -----


organization = "tulocj"
deviceType = "LORA"
deviceId = "LMT01"
appId = deviceId + "_receiver"
authMethod = "token"
authToken = "Rs3iJV)Q3zgZb+tu7)"

# Initialize the application client.
try:
	appOptions = {"org": organization, "id": appId, "auth-method": authMethod, "auth-token": authToken}
	appCli = ibmiotf.application.Client(appOptions)
except Exception as e:
	print(str(e))
	sys.exit()

# Connect and configuration the application
# - subscribe to live data from the device we created, specifically to "greeting" events
# - use the myAppEventCallback method to process events
appCli.connect()
appCli.subscribeToDeviceEvents(deviceType, deviceId, "greeting")
appCli.deviceEventCallback = myAppEventCallback

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

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    r.append(msg.topic,str(msg.payload)+'/')
    datajson=json.loads(str(msg.payload))
    print datajson['data']
    pubnub.publish().channel(msg.topic).message(datajson['data']).async(publish_callback)
    def myOnPublishCallback():
		print("Confirmed event %s received by IoTF\n" % x)
	
	success = deviceCli.publishEvent("test subj", "json", "test body", qos=0, on_publish=myOnPublishCallback)
	if not success:
		print("Not connected to IoTF")

r = redis.StrictRedis(host='localhost', port=6379, db=0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
