from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # Specify the model
        fields = ['id', 'title', 'content', 'tags', 'author']  # Specify the fields to be serialized
        read_only_fields = ['author']  # Set author as read-only (will be set in the view)

    def create(self, validated_data):
        # Automatically set the author field to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
