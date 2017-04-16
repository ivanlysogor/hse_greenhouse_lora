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

# from __future__ import print_function
import paho.mqtt.publish as publish

channelID = "258976"

apiKey = "1QKSDZUC932F8NAX"
useUnsecuredTCP = True
useUnsecuredWebsockets = False
useSSLWebsockets = False
mqttHost = "mqtt.thingspeak.com"

if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey

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
    publish.single(topic, payload='s1=10', hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)


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
