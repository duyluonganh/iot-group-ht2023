import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
import joblib
import wave
import pyaudio

'''
load_model(): 
   

Input:
    checkpoint_path(str): checkpoint path
    checkpoint_name(str): checkpoint filename
    model_name(str): name of the model

Output:
    model: Loaded model
'''


def load_model(checkpoint_path: str, checkpoint_name: str, model_name: str):
    if model_name in ['lstm', 'cnn1d', 'cnn2d']:
        # json
        model_json_path = os.path.join(checkpoint_path, checkpoint_name + '.json')
        json_file = open(model_json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)

        # Weights
        model_path = os.path.join(checkpoint_path, checkpoint_name + '.h5')
        model.load_weights(model_path)

    else:
        model_path = os.path.join(checkpoint_path, checkpoint_name + '.m')
        model = joblib.load(model_path)

    return model


'''
plotCurve(): 
    Plot loss value and accuracy curve

Input:
    train(list): Training set loss value or accuracy array
    val(list): Test set loss value or accuracy array
    title(str): 
    y_label(str): 
'''


def plotCurve(train, val, title: str, y_label: str):
    plt.plot(train)
    plt.plot(val)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


'''
play_audio(): play the audio

Input:
    file_path(str): the path to the audio
'''


def play_audio(file_path: str):
    p = pyaudio.PyAudio()
    f = wave.open(file_path, 'rb')
    stream = p.open(
        format = p.get_format_from_width(f.getsampwidth()),
        channels = f.getnchannels(),
        rate = f.getframerate(),
        output = True
    )
    data = f.readframes(f.getparams()[3])
    stream.write(data)
    stream.stop_stream()
    stream.close()
    f.close()
    
    
'''
Radar(): Confidence probability radar chart

Input:
    data_prob: probability array
    class_labels(list): Emotions
'''


def Radar(data_prob, class_labels):
    angles = np.linspace(0, 2 * np.pi, len(class_labels), endpoint = False)
    # data = np.concatenate((data_prob, [data_prob[0]]))  # closed
    # angles = np.concatenate((angles, [angles[0]]))  # closed
    # class_labels = np.concatenate((class_labels, [class_labels[0]]))  # closed
    data=data_prob


    fig = plt.figure()

    # parameter of polar
    ax = fig.add_subplot(111, polar = True)
    ax.plot(angles, data, 'bo-', linewidth=2)
    ax.fill(angles, data, facecolor='r', alpha=0.25)
    ax.set_thetagrids(angles * 180 / np.pi, class_labels)
    ax.set_title("Emotion Recognition", va = 'bottom')

    # Set the maximum value of the radar chart
    ax.set_rlim(0, 1)

    ax.grid(True)
    plt.show()

