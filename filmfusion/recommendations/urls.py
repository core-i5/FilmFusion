from django.urls import path
from .views import FetchMovieData, RecommendationAPIView

urlpatterns = [
    path('fetch/', FetchMovieData.as_view(), name='fetch'),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations')
]