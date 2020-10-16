import random
import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import datetime, timedelta

CLIENT_NAME = "sensor-pruebas"
TOPIC = "iot-sensor/test"
BROKER_PATH = ""
ROOT_CA_PATH = './AmazonRootCA1.pem'
PRIVATE_KEY_PATH = './private.pem.key'
CERTIFICATE_PATH = './certificate.pem.crt'

# Create and Configure the IoT Client
IoTclient = AWSIoTMQTTClient(CLIENT_NAME)
IoTclient.configureEndpoint(BROKER_PATH, 8883)
IoTclient.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

# Allow the device to queue infinite messages
IoTclient.configureOfflinePublishQueueing(-1)
# Number of messages to send after a connection returns
IoTclient.configureDrainingFrequency(2)  # 2 requests/second
# How long to wait for a [dis]connection to complete (in seconds)
IoTclient.configureConnectDisconnectTimeout(10)
# How long to wait for publish/[un]subscribe (in seconds)
IoTclient.configureMQTTOperationTimeout(5) 

IoTclient.connect()
IoTclient.publish(TOPIC, "connected", 0)

# Create and Send Payloads to the IoT Topic
def create_payload():
	payload = json.dumps({
        "id": int(time.time()),
        "read_date": str((datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
        "device": "python",
		"humidity": random.randint(70, 90),
		"temperature": random.randint(15, 35)
	})
	print(payload)
	return payload

while True:
	IoTclient.publish(TOPIC, create_payload(), 0)
	time.sleep(1)
    