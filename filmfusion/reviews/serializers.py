from rest_framework import serializers
from .models import Movie, Review, Comment
from .pagination import CommentPagination, ReviewPagination

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'review', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user'] 

class ReviewSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'content', 'rating', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['user'] 

    def get_comments(self, review):
        comments = review.comments.all()
        paginator = CommentPagination()
        paginated_comments = paginator.paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(paginated_comments, many=True)
        return paginator.get_paginated_response(serializer.data).data
    
    def validate_rating(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 0 and 5.')
        return value


