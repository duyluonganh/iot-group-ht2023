import subprocess

from flask import Flask, jsonify, request, make_response, redirect, url_for
import os
from werkzeug.utils import secure_filename

import iotservice
import voicerecognitionservice

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# get humidity and temperature
@app.route('/info')
def get_info():
    temperature, humidity = iotservice.get_info()
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
            'command_type': iot_command.command_type.value,
            'properties': iot_command.properties
        }
    }), 200)


@app.route('/voice_command', methods=['POST'])
def get_voice_command():
    file = request.files['file']
    filename = secure_filename(file.filename)

    os.makedirs("/audio_temp", exist_ok=True)
    path = os.path.join(os.getcwd(), "/audio_temp", filename)
    file.save(path)

    wav_path = path.replace(".3gp", ".wav")

    if (os.path.exists(wav_path)):
        os.remove(wav_path)

    subprocess.call(["ffmpeg", "-i", path, wav_path], stdout=True)

    print(path)

    result = voicerecognitionservice.get_voice_command(wav_path)

    return make_response(jsonify({
        'message': 'OK',
        'result': result
    }), 200)


if __name__ == '__main__':
    app.run()
