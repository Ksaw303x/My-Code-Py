from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys

if __name__ == '__main__':

    myMQTTClient = AWSIoTMQTTClient("Iot-test")
    myMQTTClient.configureEndpoint("a5ozrqhkdqqas-ats.iot.eu-central-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials(
        "./dev1/AmazonRootCA1.pem",
        "./dev1/dev1-private.pem.key",
        "./dev1/dev1-certificate.pem.crt"
    )

    myMQTTClient.connect()
    print("Client Connected")

    msg = "Sample data from the device"
    topic = "general/inbound"
    myMQTTClient.publish(topic, msg, 0)
    print("Message Sent")

    myMQTTClient.disconnect()
    print("Client Disconnected")
