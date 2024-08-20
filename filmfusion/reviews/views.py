from rest_framework import generics, permissions
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .pagination import ReviewPagination, CommentPagination
from rest_framework.exceptions import ValidationError

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ReviewPagination
    
    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id')
        queryset = Review.objects.all()
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        movie = serializer.validated_data.get('movie')
        user = self.request.user

        if Review.objects.filter(movie=movie, user=user).exists():
            raise ValidationError(f"You have already reviewed the movie '{movie.title}'.")
        
        serializer.save(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        return obj

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        review_id = self.request.query_params.get('review_id')
        queryset = Comment.objects.all()
        if review_id:
            queryset = queryset.filter(review_id=review_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        return obj
