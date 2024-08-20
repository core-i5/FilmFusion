from django.urls import path
from .views import (
    ReviewListCreateView, ReviewDetailView,
    CommentListCreateView, CommentDetailView
)

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<uuid:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<uuid:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
