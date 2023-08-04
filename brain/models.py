from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify

from .net import DataPointClassifier


class classifier_choices:
    SOLVERS = [
        ('adam', "adam"),
        ('sgd', "sgd"),
        ('lbfgs', "lbfgs"),
    ]

    ACTIVATIONS = [
        ('relu', "relu"),
        ('identity', "identity"),
        ('logistic', "logistic"),
        ('tanh', "tanh"),
    ]

    LEARNING_RATES = [
        ('constant', "constant"),
        ('invscaling', "invscaling"),
        ('adaptive', "adaptive"),
    ]


def choicefield(choices):
    return models.CharField(
        choices=choices,
        max_length=max([len(c) for c, _ in choices]),
        default=choices[0][0]
    )


def parse_training_warnings(warnings):
    lines = [
        f"{warning.category.__name__}: {warning.message}"
        for warning in warnings
    ]
    return '\n'.join(lines)


class Classifier(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    short_description = models.TextField(blank=True, null=True)

    hidden_layer_sizes = models.CharField(default='100', max_length=100)
    activation = choicefield(classifier_choices.ACTIVATIONS)
    solver = choicefield(classifier_choices.SOLVERS)
    alpha = models.FloatField(default=.0001)

    batch_size = models.PositiveIntegerField(blank=True, null=True)
    learning_rate = choicefield(classifier_choices.LEARNING_RATES)
    learning_rate_init = models.FloatField(default=.001)
    power_t = models.FloatField(default=.5)

    max_iter = models.PositiveIntegerField(default=200)
    shuffle = models.BooleanField(default=True)
    random_state = models.PositiveIntegerField(null=True, blank=True)
    tol = models.FloatField(default=1e-4)

    verbose = models.BooleanField(default=False)
    warm_start = models.BooleanField(default=False)
    momentum = models.FloatField(default=.9)
    nesterovs_momentum = models.BooleanField(default=True)

    early_stopping = models.BooleanField(default=False)
    validation_fraction = models.FloatField(default=.1)
    beta_1 = models.FloatField(default=.9)
    beta_2 = models.FloatField(default=.999)

    epsilon = models.FloatField(default=1e-8)
    n_iter_no_change = models.PositiveIntegerField(default=10)
    max_fun = models.PositiveIntegerField(default=15000)

    neural_net = models.FileField(null=True)
    scaler = models.FileField(null=True)
    training_warnings = models.TextField(null=True, editable=False)

    def train(self):
        net_data, scaler_data, training_warnings = self.get_classifier().train(self.data_points.all())

        self.neural_net.delete()
        self.neural_net.save(f"net_{self.slug}", ContentFile(net_data))

        self.scaler.delete()
        self.scaler.save(f"scaler_{self.slug}", ContentFile(scaler_data))

        self.training_warnings = parse_training_warnings(training_warnings)
        self.save()

    def classify(self, sample):
        return self.get_classifier(load=True).classify(sample)

    def save(self, *args, **kwargs):
        # TODO: only allow changes to samples and features when there are no data points
        # TODO: also add a feature to make a config unavailable for register
        # this allows a workflow of disable -> delete data -> change samples/features
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
            
    def get_classifier(self, load=False):
        if load:
            return DataPointClassifier(
                load_from_db_instance=self
            )
        else:
            return DataPointClassifier(
                hidden_layer_sizes=[int(size.strip()) for size in self.hidden_layer_sizes.split(',')],
                activation=self.activation,
                solver=self.solver,
                alpha=self.alpha,

                batch_size=self.batch_size or 'auto',
                learning_rate=self.learning_rate,
                learning_rate_init=self.learning_rate_init,
                power_t=self.power_t,

                max_iter=self.max_iter,
                shuffle=self.shuffle,
                random_state=self.random_state,
                tol=self.tol,

                verbose=self.verbose,
                warm_start=self.warm_start,
                momentum=self.momentum,
                nesterovs_momentum=self.nesterovs_momentum,

                early_stopping=self.early_stopping,
                validation_fraction=self.validation_fraction,
                beta_1=self.beta_1,
                beta_2=self.beta_2,

                epsilon=self.epsilon,
                n_iter_no_change=self.n_iter_no_change,
                max_fun=self.max_fun,
            )

    def __str__(self):
        return self.name


class ClassifierSample(models.Model):
    config = models.ForeignKey(
        Classifier,
        related_name='samples',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ClassifierFeature(models.Model):
    config = models.ForeignKey(
        Classifier,
        related_name='features',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    config = models.ForeignKey(
        Classifier,
        related_name='data_points',
        on_delete=models.CASCADE
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    samples = models.JSONField()
    features = models.JSONField()

    @property
    def sample_list(self):
        return [v for (k, v) in self.samples.items()]

    @property
    def feature_list(self):
        return [v for (k, v) in self.features.items()]

    def __str__(self):
        return str(self.timestamp)
