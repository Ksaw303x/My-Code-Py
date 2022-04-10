import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def customCallback(client, userdata, message):
    print("callback came...")
    print(message.payload)


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

    myMQTTClient.subscribe("general/outbound", 1, customCallback)
    print('waiting for the callback. Click to conntinue...')
    x = input()

    myMQTTClient.unsubscribe("general/outbound")
    print("Client unsubscribed")

    myMQTTClient.disconnect()
    print("Client Disconnected")
