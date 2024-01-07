import sys
from sklearn.metrics import accuracy_score


class Common_Model(object):

    def __init__(self, save_path: str = '', name: str = 'Not Specified'):
        self.model = None
        self.trained = False # check

    '''
    train(): Train a model on a given training set

        Input:
        x_train: Training set samples
        y_train: Training set label
        x_val: Test set samples
        y_val: Test set label

    '''
    def train(self, x_train, y_train, x_val, y_val):
        raise NotImplementedError()

    '''
    predict(): Recognizing emotions in audio

    Input:
        samples: Audio features to be identified

    Output:
        list: List of recognition results (labels)
    '''
    def predict(self, samples):
        raise NotImplementedError()
        
    '''
    predict_proba(): Confidence probability of audio emotion

    Input:
        samples: 



    Output:
        list: 
    '''
    def predict_proba(self, samples):
        if not self.trained:
            sys.stderr.write("No Model.")
            sys.exit(-1)
        return self.model.predict_proba(samples)

    '''
    save_model(): Store the model named model_name under the path config.checkpoint_path
    '''
    def save_model(self, model_name: str):
        raise NotImplementedError()

    '''
    evaluate(): Evaluate the model on the test set and output the accuracy
98
    Input:
        x_test: Samples
        y_test: Lables
    '''
    def evaluate(self, x_test, y_test):

        predictions = self.predict(x_test)
        print(y_test)
        print(predictions)
        print('Accuracy: %.3f\n' % accuracy_score(y_pred = predictions, y_true = y_test))
 
        '''
        predictions = self.predict(x_test)
        score = self.model.score(x_test, y_test)
        print("True Lable: ", y_test)
        print("Predict Lable: ", predictions)
        print("Score: ", score)
        '''