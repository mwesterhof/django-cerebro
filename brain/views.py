from rest_framework import generics
from rest_framework.response import Response

from .models import VisitorBehavior
from .net import VisitorClassifier
from .serializers import VisitorBehaviorSerializer, VisitorBehaviorSerializerForPrediction


class VisitorBehaviorListCreate(generics.ListCreateAPIView):
    queryset = VisitorBehavior.objects.all()
    serializer_class = VisitorBehaviorSerializer


class PredictionView(generics.GenericAPIView):
    serializer_class = VisitorBehaviorSerializerForPrediction

    def post(self, request, format=None):
        creation_kwargs = {k: v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'}
        behavior = VisitorBehavior(**creation_kwargs)
        prediction = VisitorClassifier().predict_conversion([behavior])

        creation_kwargs['conversion_target_a'] = prediction[0][0]
        creation_kwargs['conversion_target_b'] = prediction[0][1]

        serializer = self.serializer_class(VisitorBehavior(**creation_kwargs))
        return Response(serializer.data)
