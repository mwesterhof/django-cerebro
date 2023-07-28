from django.conf import settings
from django.core.files import File

from .models import VisitorBehavior
from sklearn.neural_network import MLPClassifier
import pickle

NET_PATH = settings.NET_PATH


class VisitorClassifier:
    def __init__(self, load=True, train=False):
        if load:
            self.load()
        else:
            self.initialize()

        if train:
            self.train()

    def initialize(self, solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1):
        self.net = MLPClassifier(
            solver=solver,
            alpha=alpha,
            hidden_layer_sizes=hidden_layer_sizes,
            random_state=random_state
        )

    def train(self):
        visitors = VisitorBehavior.objects.all()
        X = [visitor.sample for visitor in visitors]
        y = [visitor.feature for visitor in visitors]

        self.net.fit(X, y)

    def predict_conversion(self, visitors):
        behaviors = [visitor.sample for visitor in visitors]
        return self.net.predict(behaviors)

    def save(self):
        with open(NET_PATH, 'wb') as outf:
            file_obj = File(outf)
            pickle.dump(self.net, file_obj)

    def load(self):
        with open(NET_PATH, 'rb') as inf:
            self.net = pickle.load(inf)

    def reload(self):
        self.load()
