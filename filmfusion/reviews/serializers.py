from rest_framework import serializers
from .models import Movie, Review, Comment
from .pagination import CommentPagination, ReviewPagination

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'content', 'rating', 'created_at', 'updated_at', 'comments']

    def get_comments(self, review):
        comments = review.comments.all()
        paginated_comments = CommentPagination().paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(paginated_comments, many=True)
        return self.context['request'].pagination_class.get_paginated_response(serializer.data).data
    
    def validate_rating(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError('Rating must be between 0 and 10.')
        return value


