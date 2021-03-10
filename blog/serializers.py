from rest_framework import serializers
from . models import Category, Post, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())

    posts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Post.objects.all())

    comments = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Comment.objects.all())

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'categories', 'posts', 'comments', 'owner']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
