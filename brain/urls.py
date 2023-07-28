from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PredictionView, VisitorBehaviorListCreate


urlpatterns = format_suffix_patterns([
    path('register/', VisitorBehaviorListCreate.as_view()),
    path('predict/', PredictionView.as_view()),
])
