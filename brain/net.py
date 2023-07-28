import pickle

from django.conf import settings
from django.core.files import File

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from .models import VisitorBehavior


BRAIN_PATH = settings.NET_PATH / 'brain.net'
SCALER_PATH = settings.NET_PATH / 'scaler.net'


class VisitorClassifier:
    def __init__(self, load=True, train=False):
        if load:
            self.load()
        else:
            self.initialize()

        if train:
            self.train()

    def initialize(self, solver='sgd', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1, max_iter=10000):
        self.net = MLPClassifier(
            solver=solver,
            alpha=alpha,
            hidden_layer_sizes=hidden_layer_sizes,
            random_state=random_state,
            max_iter=max_iter,
        )
        self.scaler = StandardScaler()

    def train(self):
        visitors = VisitorBehavior.objects.all()
        X = [visitor.sample for visitor in visitors]
        y = [visitor.feature for visitor in visitors]

        self.scaler.fit(X)
        X = self.scaler.transform(X)

        self.net.fit(X, y)

    def predict_conversion(self, visitors):
        behaviors = [visitor.sample for visitor in visitors]
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
