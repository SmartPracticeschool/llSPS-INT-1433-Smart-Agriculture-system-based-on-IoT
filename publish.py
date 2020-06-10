import time
import sys
import ibmiotf
import ibmiotf.application
import ibmiotf.device

organization='a5yxee'
deviceType='iotdevice'
deviceId='motor'
authMethod='token'
authToken='******'

def myCommandCallback(cmd):
    print('Command received: %s' % cmd.data)
    if cmd.data['command']=='motoron':
        print('MOTOR ON')
    elif cmd.data['command']=='motoroff':
        print('MOTOR OFF')
    data={'Command' : cmd.data['command']}
    success=deviceCli.publishEvent('event', 'json' ,data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not Connected to IoTF")
    myCommandCallback.has_been_called = True
try:
    deviceOptions= {"org": organization, 'type': deviceType, 'id': deviceId, 'auth-method': authMethod, 'auth-token': authToken}
    deviceCli=ibmiotf.device.Client(deviceOptions)
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()
deviceCli.connect()

while True:
    myCommandCallback.has_been_called= False
    status='Sensor is ON'
    data={'Status': status}
    connected=False
    def myOnPublishCallback():
        print(data,"to IBM Watson")
        connected=True
    if not connected:
        success=deviceCli.publishEvent('event', 'json' ,data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(1)
    deviceCli.commandCallback = myCommandCallback
    if myCommandCallback.has_been_called:
        print("CALL MADE")
