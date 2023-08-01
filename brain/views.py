from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from .models import ClassifierConfig, DataPoint
from .net import DataPointClassifier
from .serializers import get_serializer_from_config, DataPointSerializerForPrediction


class DataPointCreate(generics.ListCreateAPIView):
    def get_config(self):
        return get_object_or_404(ClassifierConfig, slug=self.kwargs['slug'])

    def dispatch(self, *args, **kwargs):
        self.config = self.get_config()
        return super().dispatch(*args, **kwargs)

    def get_serializer_class(self):
        return get_serializer_from_config(self.config)

    def get_queryset(self, *args, **kwargs):
        return DataPoint.objects.filter(config=self.config)


class PredictionView(generics.GenericAPIView):
    serializer_class = DataPointSerializerForPrediction

    def post(self, request, format=None):
        creation_kwargs = {k: v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'}
        behavior = DataPoint(**creation_kwargs)
        prediction = DataPointClassifier().predict_conversion([behavior])

        creation_kwargs['conversion_target_a'] = prediction[0][0]
        creation_kwargs['conversion_target_b'] = prediction[0][1]

        serializer = self.serializer_class(DataPoint(**creation_kwargs))
        return Response(serializer.data)
