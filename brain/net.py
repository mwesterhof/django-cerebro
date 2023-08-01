import io
import pickle
from warnings import catch_warnings

from django.conf import settings
from django.core.files import File

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


BRAIN_PATH = settings.NET_PATH / 'brain.net'
SCALER_PATH = settings.NET_PATH / 'scaler.net'


class DataPointClassifier:
    def __init__(self, *args, **kwargs):
        self.scikit_classifier = MLPClassifier(*args, **kwargs)

    def train(self, data_points):
        X = [point.sample_list for point in data_points]
        y = [point.feature_list for point in data_points]

        scaler = StandardScaler()
        scaler.fit(X)

        X = scaler.transform(X)
        with catch_warnings(record=True) as training_warnings:
            self.scikit_classifier.fit(X, y)
        
        with io.BytesIO() as net_buffer:
            net_file = File(net_buffer)
            pickle.dump(self.scikit_classifier, net_file)

        with io.BytesIO() as scaler_buffer:
            scaler_file = File(scaler_buffer)
            pickle.dump(scaler, scaler_file)

        return net_file, scaler_file, training_warnings

    def predict_conversion(self, data_points):
        behaviors = [point.sample for point in data_points]
        behaviors = self.scaler.transform(behaviors)
        return self.net.predict(behaviors)

    def save(self):
        with open(BRAIN_PATH, 'wb') as outf:
            file_obj = File(outf)
            pickle.dump(self.net, file_obj)

        with open(SCALER_PATH, 'wb') as outf:
            file_obj = File(outf)
            pickle.dump(self.scaler, file_obj)

    def load(self):
        with open(BRAIN_PATH, 'rb') as inf:
            self.net = pickle.load(inf)
        with open(SCALER_PATH, 'rb') as inf:
            self.scaler = pickle.load(inf)

    def reload(self):
        self.load()
