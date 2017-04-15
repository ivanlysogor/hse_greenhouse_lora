import paho.mqtt.client as mqtt
import json
import redis


publish_key   = "pub-c-2272ef16-05d2-4cfb-927a-7a7c4232145b"
subscribe_key = "sub-c-b4c7721e-2229-11e7-bd07-02ee2ddab7fe"
channel_name  = "devices/lora/807B85902000017A/lmt01"
client_uuid   = "1ddb86ef5"

mqtt_hostname = "mqtt.pubnub.com"
mqtt_connect  = publish_key + "/" + subscribe_key + "/" + client_uuid
mqtt_topic    = publish_key + "/" + subscribe_key + "/" + channel_name

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
    mosq_object.publish( mqtt_topic, msg.payload)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

mosq_object = mqtt.Client()
mosq_object.connect(mqtt_hostname, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
