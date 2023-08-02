import pickle
from warnings import catch_warnings

from django.conf import settings
from django.core.files import File

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


class DataPointClassifier:
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('load_from_db_instance')

        if instance:
            self.scikit_classifier = pickle.load(instance.neural_net)
            self.scaler = pickle.load(instance.scaler)
        else:
            self.scikit_classifier = MLPClassifier(*args, **kwargs)
            self.scaler = StandardScaler()

    def train(self, data_points):
        X = [point.sample_list for point in data_points]
        y = [point.feature_list for point in data_points]

        self.scaler.fit(X)

        X = scaler.transform(X)
        with catch_warnings(record=True) as training_warnings:
            self.scikit_classifier.fit(X, y)
        
        net_data = pickle.dumps(self.scikit_classifier)
        scaler_data = pickle.dumps(scaler)

        return net_data, scaler_data, training_warnings

    def classify(self, sample):
        X = self.scaler.transform(sample)
        return self.scikit_classifier.predict(X)
