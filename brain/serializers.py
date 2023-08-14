from rest_framework import serializers

from .models import DataPoint


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ['id', 'timestamp', 'samples', 'features']


class DynamicDataPointSerializerBase(serializers.Serializer):
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


def get_serializer_from_config(config, readonly_features=False):
    return type(
        'DataPointSerializer',
        (DynamicDataPointSerializerBase,),
        dict(
            [
                ('config', config)
            ] + [
                (sample.name, serializers.IntegerField())
                for sample in config.samples.all()
            ] + [
                (feature.name, serializers.IntegerField(read_only=readonly_features))
                for feature in config.features.all()
            ]
        )
    )
