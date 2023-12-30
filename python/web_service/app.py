from flask import Flask, jsonify, request, make_response

import iotservice
import voicerecognitionservice

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

#get humidity and temperature
@app.route('/info')
def get_info():
    humidity = iotservice.get_humidity()
    temperature = iotservice.get_temperature()
    return jsonify({
        'message': 'OK',
        'humidity': humidity,
        'temperature': temperature
    })

@app.route('/command', methods=['POST'])
def get_command():
    query = request.args.get('query')
    iot_command = voicerecognitionservice.get_iot_command(query)
    return make_response(jsonify({
        'message': 'OK',
        'command': {
            'command_type' : iot_command.command_type.value,
            'properties' : iot_command.properties
        }
    }), 200)

if __name__ == '__main__':
    app.run()
