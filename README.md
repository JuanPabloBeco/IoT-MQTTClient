IoT-MQTTClient

Here there are several customizable Python MQTT clients.

Now two versions of an echo test for new devices are offered using paho-mqtt. The first paho_echo_client is a simple echo, after a message it sends it back with "echo-" at the beginning.

The extended version sends all messages back in the same topic and also sends all of them to a central topic("server_topic" by default). 
As another functionality it counts the words of the messages sent and sends the information to a specific topic("message_length" by default).