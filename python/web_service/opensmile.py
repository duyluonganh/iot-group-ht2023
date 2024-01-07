import os
import csv
import sys
import subprocess
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.model_selection import train_test_split

# Number of features per feature set
FEATURE_NUM = {'IS10_paraling': 1582}

'''
get_feature_opensmile(): Opensmile Extract features from an audio

Input:
    config(Class)
    file_path: 

Output：
    The feature vector of this audio
'''


def get_feature_opensmile(config, filepath: str):
    # csv file used to store the characteristics of an audio
    single_feat_path = 'E:/CSS/IoT/reference/speech-emotion-recognition-master (3)/speech-emotion-recognition-master/features/single_feature.csv'
    # Opensmile configuration file path,we use IS10_paraling
    opensmile_config_path = os.path.join(config.opensmile_path, 'config/is09-13/IS10_paraling.conf')
    cmd3 = 'SMILExtract -C ' + opensmile_config_path + ' -I ' + filepath + ' -O ' + single_feat_path
    cmd = subprocess.Popen(cmd3, cwd=config.opensmile_path + 'bin', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True).communicate()[0]
    reader = csv.reader(open(single_feat_path, 'r'))
    rows = [row for row in reader]
    last_line = rows[-1]
    return last_line[1: FEATURE_NUM[config.opensmile_config] + 1]


'''
load_feature(): Load feature data from a .csv file

Input:
    config(Class)
    feature_path: Feature file path
    train: It is a training data，or not

Output:
    Training data, test data and corresponding labels
'''


def load_feature(config, feature_path: str, train: bool):
    # Load feature data
    df = pd.read_csv(feature_path)
    features = [str(i) for i in range(1, FEATURE_NUM[config.opensmile_config] + 1)]

    X = df.loc[:, features].values
    Y = df.loc[:, 'label'].values

    # Standardized model path
    scaler_path = os.path.join(config.checkpoint_path, 'SCALER_OPENSMILE.m')

    if train == True:
        # normalized
        scaler = StandardScaler().fit(X)
        # save the model
        joblib.dump(scaler, scaler_path)
        X = scaler.transform(X)

        # split
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        return x_train, x_test, y_train, y_test
    else:
        # Load standardized model
        scaler = joblib.load(scaler_path)
        X = scaler.transform(X)
        return X


'''
get_data(): 
    Extract the features of all audios: traverse all folders, 
    read the audios in each folder, extract the features of each audio, 
    and save all features in feature_path

Input:
    config(Class)
    data_path: Dataset folder/path of the file for test 
    feature_path: Path to save features
    train: It is the training data,or not

Output:
    train = True: Training data, test data features and corresponding labels
    train = False: Predictive data features
'''


# Opensmile for the features
def get_data(config, data_path, feature_path: str, train: bool):
    writer = csv.writer(open(feature_path, 'w'))
    first_row = ['label']
    for i in range(1, FEATURE_NUM[config.opensmile_config] + 1):
        first_row.append(str(i))
    writer.writerow(first_row)

    writer = csv.writer(open(feature_path, 'a+'))
    print('Opensmile extracting...')

    if train == True:
        cur_dir = os.getcwd()
        sys.stderr.write('Curdir: %s\n' % cur_dir)
        os.chdir(data_path)
        # 遍历文件夹
        for i, directory in enumerate(config.class_labels):
            sys.stderr.write("Started reading folder %s\n" % directory)
            os.chdir(directory)

            # label_name = directory
            label = config.class_labels.index(directory)

            # 读取该文件夹下的音频
            for filename in os.listdir('.'):
                if not filename.endswith('wav'):
                    continue
                filepath = os.path.join(os.getcwd(), filename)

                # 提取该音频的特征
                feature_vector = get_feature_opensmile(config, filepath)
                feature_vector.insert(0, label)
                # 把每个音频的特征整理到一个 csv 文件中
                writer.writerow(feature_vector)

            sys.stderr.write("Ended reading folder %s\n" % directory)
            os.chdir('..')
        os.chdir(cur_dir)

    else:
        feature_vector = get_feature_opensmile(config, data_path)
        feature_vector.insert(0, '-1')
        writer.writerow(feature_vector)

    print('Opensmile extract done.')

    if train:
        return load_feature(config, feature_path, train=train)
