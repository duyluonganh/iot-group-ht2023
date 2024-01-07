import os
import numpy as np
from keras.utils import np_utils
import models
import opensmile as of
import utils.opts as opts

'''
train(): train the model
Input: config(Class)
Output: trained model
'''


def train(config):
    # Load features preprocessed by preprocess.py
    x_train, x_test, y_train, y_test = of.load_feature(config, config.train_feature_path, train=True)

    # Build
    model = models.setup(config=config, n_feats=x_train.shape[1])

    # Train
    print('----- start training', config.model, '-----')
    y_train, y_val = np_utils.to_categorical(y_train), np_utils.to_categorical(y_test) # One-Hot
    model.train(
        x_train, y_train,
        x_test, y_val,
        batch_size=config.batch_size,
        n_epochs=config.epochs
    )
    print('----- end training ', config.model, ' -----')

    # Validate
    model.evaluate(x_test, y_test)
    # Save
    model.save_model(config)


if __name__ == '__main__':
    config = opts.parse_opt()
    train(config)

