import paho.mqtt.client as mqtt
from my_globals import *
import my_sqlite

QOS_AT_MOST_ONCE=0
QOS_AT_LEAST_ONCE=1
QOS_EXACTLY_ONCE=2

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if DEBUG: print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    (result, mid) = client.subscribe("bikesensor/rotate", qos=QOS_EXACTLY_ONCE)
    if DEBUG: print(f'Result: {result} : Mid: {mid}')
    # client.on_subscribe = on_subscription

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    g_event_list.append(msg.payload)
    my_sqlite.write_instant_data_to_sqlite(1)
    if DEBUG: print(f'From topic: {msg.topic} -> {msg.payload}')

def on_subscription(client, userdata, mid, granted_qos):
    if DEBUG: print(f'on_subscription: {client}, {userdata}, {mid}, {granted_qos}')


def init_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('mqtt', '12345678')
    client.connect("192.168.1.75", 1883, 60)
    client.loop_start()