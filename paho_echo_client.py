import paho.mqtt.client as mqtt

# When server echoes a message always add serverPrefix at the start
SERVER_PREFIX = "echo-"
TOPICS_TO_LISTEN = [
    "test1",
    "test2"
]

#BROKER_IP_OR_URL = "52.26.212.38" #AWS MQTT Server Oregon
BROKER_IP_OR_URL = "18.228.161.6" #AWS MQTT Server Sao Paulo

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in TOPICS_TO_LISTEN:
        client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    incoming_message = msg.payload.decode("utf-8")

    print("Topic:"+msg.topic)
    print("Incoming:"+incoming_message)

    if incoming_message.find(SERVER_PREFIX) != 0:
        client.publish(msg.topic, SERVER_PREFIX+incoming_message)
        print("Response: "+SERVER_PREFIX+incoming_message)
        print("")
    else:
        print("Response: No")
        print("----------")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP_OR_URL, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()