import pickle
from collections.abc import Iterable
from warnings import catch_warnings

from django.conf import settings
from django.core.files import File

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


def _scikit_1d_workaround(values):
    if len(values[0]) == 1:
        # every sample contains only one value
        # scikit_learn expects a 1d list in this case, for some reason
        return [i[0] for i in values]
    return values


class DataPointClassifier:
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('load_from_db_instance', None)

        if instance:
            self.scikit_classifier = pickle.load(instance.neural_net)
            self.scaler = pickle.load(instance.scaler)
        else:
            self.scikit_classifier = MLPClassifier(*args, **kwargs)
            self.scaler = StandardScaler()

    def train(self, data_points):
        X = _scikit_1d_workaround([point.sample_list for point in data_points])
        y = _scikit_1d_workaround([point.feature_list for point in data_points])

        self.scaler.fit(X)
        X = self.scaler.transform(X)

        with catch_warnings(record=True) as training_warnings:
            self.scikit_classifier.fit(X, y)
        
        net_data = pickle.dumps(self.scikit_classifier)
        scaler_data = pickle.dumps(self.scaler)

        return net_data, scaler_data, training_warnings

    def classify(self, sample):
        X = self.scaler.transform(_scikit_1d_workaround(sample))
        feature_raw = self.scikit_classifier.predict(X)
        if not isinstance(feature_raw[0], Iterable):
            return [[i] for i in feature_raw]
        else:
            return feature_raw
