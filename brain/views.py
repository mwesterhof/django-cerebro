from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from .models import Classifier, DataPoint
from .net import DataPointClassifier
from .serializers import get_serializer_from_config


class DynamicSerializerViewMixin:
    def dispatch(self, *args, **kwargs):
        self.config = self.get_config()
        return super().dispatch(*args, **kwargs)

    def get_config(self):
        return get_object_or_404(Classifier, slug=self.kwargs['slug'])

    def get_serializer_class(self):
        return get_serializer_from_config(self.config)


class DataPointCreate(DynamicSerializerViewMixin, generics.ListCreateAPIView):
    def get_queryset(self, *args, **kwargs):
        return DataPoint.objects.filter(config=self.config)


class PredictionView(DynamicSerializerViewMixin, generics.GenericAPIView):
    def get_serializer_class(self):
        return get_serializer_from_config(self.config, readonly_features=True)

    def post(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        request_serializer = serializer_class(data=request.data)

        if request_serializer.is_valid():
            sample = list(request_serializer.validated_data.values())
            feature = self.config.classify([sample])[0]
            datapoint_kwargs = {}

            for i, sample_name in enumerate(self.config.samples.values_list('name', flat=True)):
                datapoint_kwargs[sample_name] = sample[i]

            for i, feature_name in enumerate(self.config.features.values_list('name', flat=True)):
                datapoint_kwargs[feature_name] = feature[i]

            return Response(datapoint_kwargs)

        return super().post(request, **kwargs)
