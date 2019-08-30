import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import settings

import os

BROKER_IP_OR_URL = os.getenv("BROKER_IP_OR_URL")
NUMBER_OF_TESTS = 10


from datetime import datetime, timedelta

TOPIC = "latency_test"
PAYLOAD = "test payload"

class latency_test:
    
    def __init__(self, number_of_tests=10):
        
        self.current_sent_datetime = timedelta()
        self.current_received_datetime = timedelta()
        self.tests_sent_datetime = []
        self.tests_received_datetime = []
        self.tests_latency = []
        self.latency = timedelta()
        self.number_of_tests=number_of_tests
        self.number_of_tests_remaining=number_of_tests

    def start(self):
        print("====================")
        print("MQTT latency test\n")
        print("Connected with " + BROKER_IP_OR_URL)
        # print("Connected with result code "+str(rc))
        self.start_test()

    def restart(self):
        self.current_sent_datetime = timedelta()
        self.current_received_datetime = timedelta()
        self.tests_sent_datetime = []
        self.tests_received_datetime = []
        self.tests_latency = []
        self.latency = timedelta()
        self.number_of_tests_remaining=self.number_of_tests
        self.start()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(TOPIC)
        self.start()
            

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        incoming_message = msg.payload.decode("utf-8")

        if msg.topic == TOPIC and incoming_message == PAYLOAD:
            time_of_arrival = datetime.now()
            self.current_received_datetime = time_of_arrival

            #print("Received at " + self.current_received_datetime.strftime("%H:%M:%S"))

            self.process_test()

    def process_test(self):
        #print("Received at " + self.current_received_datetime.strftime("%H:%M:%S"))

        self.tests_received_datetime.append(self.current_received_datetime)
        self.tests_sent_datetime.append(self.current_sent_datetime)

        self.tests_latency.append((self.current_received_datetime-self.current_sent_datetime))
        self.latency += (self.current_received_datetime-self.current_sent_datetime)/self.number_of_tests
        #print("Latency: " + str((self.current_received_datetime-self.current_sent_datetime)))

        self.number_of_tests_remaining -= 1

        if self.number_of_tests_remaining != 0:
            self.start_test()
        else:
            print("Number of Tests: " + str(self.number_of_tests))
            print("Latency: " + str(self.latency.microseconds/1000) + "ms")
            print("====================")

    def start_test(self):
        #print("Sent at " + self.current_sent_datetime.strftime("%H:%M:%S"))
        self.current_sent_datetime = datetime.now()
        client.publish(TOPIC, PAYLOAD)

sent_datetime=0
received_datetime=0

client = mqtt.Client()

test = latency_test(NUMBER_OF_TESTS)
client.on_connect = test.on_connect
client.on_message = test.on_message

client.connect(BROKER_IP_OR_URL, 1883, 60)

client.loop_forever()