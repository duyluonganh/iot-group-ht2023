import numpy as np
from utils.common import load_model,play_audio
import opensmile as of
import utils.opts as opts


def reshape_input(data):
    data = np.reshape(data, (data.shape[0], data.shape[1], 1))
    return data


'''
predict(): Predict audio sentiment

Input:
    config(Class)
    audio_path: audio path to predict
	model: loaded model

Output: Results and confidence probability
'''


def predict(config, audio_path, model):
    play_audio(audio_path)
    of.get_data(config, audio_path, config.predict_feature_path, train=False)
    test_feature = of.load_feature(config, config.predict_feature_path, train=False)

    test_feature = reshape_input(test_feature)

    result = model.predict(test_feature)
    result = np.argmax(result)

    result_prob = model.predict(test_feature)[0]

    print('Recogntion: ', config.class_labels[int(result)])
    print('Probability: ', result_prob)

def predict_for_ws(audio_path):
    #audio_path = 'E:/CSS/IoT/reference/speech-emotion-recognition-master (3)/speech-emotion-recognition-master/dataset/RAVDESS_1s_4categories/sad/3-2.wav'

    config = opts.parse_opt()

    # Load model
    model = load_model(
        checkpoint_path=config.checkpoint_path,
        checkpoint_name=config.checkpoint_name,
        model_name=config.model
    )

    return predict(config, audio_path, model)

if __name__ == '__main__':
    audio_path = 'E:/CSS/IoT/reference/speech-emotion-recognition-master (3)/speech-emotion-recognition-master/dataset/RAVDESS_1s_4categories/sad/3-2.wav'

    config = opts.parse_opt()

    # Load model
    model = load_model(
        checkpoint_path=config.checkpoint_path,
        checkpoint_name=config.checkpoint_name,
        model_name=config.model
    )

    predict(config, audio_path, model)
