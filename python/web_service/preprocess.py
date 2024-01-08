'''
Extract features of the audio in the dataset and save them
'''

import opensmile as of
import utils.opts as opts


if __name__ == '__main__':

    config = opts.parse_opt()

    of.get_data(config, config.data_path, config.train_feature_path, train=True)
