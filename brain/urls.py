from django.conf import settings
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PredictionView, DataPointCreate, DataPointList


urlpatterns = format_suffix_patterns([
    path('<slug:slug>/', DataPointList.as_view(), name='list'),
    path('<slug:slug>/register/', DataPointCreate.as_view(), name='register'),
    path('<slug:slug>/predict/', PredictionView.as_view(), name='predict'),
])
