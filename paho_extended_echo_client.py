import paho.mqtt.client as mqtt
import settings

import os
BROKER_IP_OR_URL = os.getenv("BROKER_IP_OR_URL")

# When server echoes a message always add serverPrefix at the start
SERVER_PREFIX = "echo-"
TOPICS_TO_LISTEN = [
    "test1",
    "test2"
]
TOPIC_TO_SEND_INCOMING_MESSAGE_LENGHT = "message_lenght"

SERVER_ONLINE_TOPIC = "server_topic"
SERVER_ONLINE_MESSAGE = "Hi!"
SERVER_DISABLE_ECHO_MESSAGE = "disable_echo"
SERVER_ENABLE_ECHO_MESSAGE = "enable_echo"
server_echo_flag = True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in TOPICS_TO_LISTEN:
        client.subscribe(topic)

    client.publish(SERVER_ONLINE_TOPIC, SERVER_ONLINE_MESSAGE)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    incoming_message = msg.payload.decode("utf-8")

    print("Topic:" + msg.topic)
    print("Incoming:" + incoming_message)

    handle_echo_abailability(incoming_message)

    print(server_echo_flag)

    if incoming_message.find(SERVER_PREFIX) != 0 and server_echo_flag == True:
        client.publish(SERVER_ONLINE_TOPIC, SERVER_PREFIX + incoming_message)
        client.publish(msg.topic, SERVER_PREFIX+incoming_message)
        client.publish(TOPIC_TO_SEND_INCOMING_MESSAGE_LENGHT, len(incoming_message))
        print("Response: " + SERVER_PREFIX + incoming_message)
        print("")
    else:
        print("Response: No")
        print("----------")

def handle_echo_abailability(incoming_message):
    if incoming_message.find(SERVER_DISABLE_ECHO_MESSAGE) == 0:
        server_echo_flag = False
        print("Echo disabled")
    elif incoming_message.find(SERVER_ENABLE_ECHO_MESSAGE) == 0:
        server_echo_flag = True
        print("Echo enabled")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP_OR_URL, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
