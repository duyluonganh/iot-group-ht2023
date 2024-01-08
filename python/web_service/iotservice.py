import json
from random import random, randint
import paramiko


def get_info():  # call rasberi Pi to get humidity
    hostname = '192.168.137.48'
    port = 22

    username = 'admin'
    password = 'admin'

    cmd = 'python device_info.py'

    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        client.connect(hostname, port, username, password)

        (stdin, stdout, stderr) = client.exec_command(cmd)

        output = stdout.readlines()
        client.close()

        if len(output) == 0: #sometimes, there are too many requests then API call to teldus will fail then we reserve this backup
            output = json.dumps({
                "battery": "254",
                "clientName": "iotworkshop1 - tellstick znet",
                "data": [
                    {
                        "lastUpdated": 1700235028,
                        "max": "29.3",
                        "maxTime": 1638799531,
                        "min": "16.7",
                        "minTime": 1642045253,
                        "name": "temp",
                        "scale": "0",
                        "value": "23.1"
                    },
                    {
                        "lastUpdated": 1700235028,
                        "max": "60",
                        "maxTime": 1636617767,
                        "min": "20",
                        "minTime": 1638448367,
                        "name": "humidity",
                        "scale": "0",
                        "value": "24"
                    }
                ],
                "editable": 1,
                "id": "1547943570",
                "ignored": 0,
                "keepHistory": "0",
                "lastUpdated": 1700235028,
                "name": "tempsensor18-ch4",
                "protocol": "fineoffset",
                "sensorId": "42",
                "timezoneoffset": 3600
            })
        temp = json.loads(output)['data'][0]['value']
        humidity = json.loads(output)['data'][1]['value']
        return temp, humidity
    return randint(-10, 20), randint(-10, 20)
