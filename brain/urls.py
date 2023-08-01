from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PredictionView, DataPointCreate


urlpatterns = format_suffix_patterns([
    path('<slug:slug>/register/', DataPointCreate.as_view()),
    path('<slug:slug>/predict/', PredictionView.as_view()),
])
