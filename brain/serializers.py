from rest_framework import serializers

from .models import DataPoint


class DataPointSerializerBase(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sample_names = self.config.samples.values_list('name', flat=True)
        self.feature_names = self.config.features.values_list('name', flat=True)

    def create(self, validated_data):
        data = {
            'config': self.config,
            'samples': {k: v for k, v in validated_data.items() if k in self.sample_names},
            'features': {k: v for k, v in validated_data.items() if k in self.feature_names},
        }

        return DataPoint.objects.create(**data)

    def to_representation(self, instance):
        result = {}

        for sample in self.sample_names:
            result[sample] = instance.samples[sample]
        for feature in self.feature_names:
            result[feature] = instance.features[feature]

        return result


def get_serializer_from_config(config):
    return type(
        'DataPointSerializer',
        (DataPointSerializerBase,),
        dict(
            [
                ('config', config)
            ] + [
                (sample.name, serializers.IntegerField())
                for sample in config.samples.all()
            ] + [
                (feature.name, serializers.IntegerField())
                for feature in config.features.all()
            ]
        )
    )


class DataPointSerializerForPrediction(serializers.Serializer):
    time_spent = serializers.IntegerField()
    pages_visited = serializers.IntegerField()

    conversion_target_a = serializers.IntegerField(read_only=True)
    conversion_target_b = serializers.IntegerField(read_only=True)
