from django.shortcuts import render
from blog.models import Post, Comment, Category
from .forms import CommentForm

from . serializers import CategorySerializer, PostSerializer, CommentSerializer
from rest_framework.response import Response

from rest_framework.views import APIView

from django.http import Http404
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer

"""Pages: blog_index , blog_category, blog_details"""


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts
    }
    return render(request, 'blog_index.html', context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category).order_by('-created_on')
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, 'blog_category.html', context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form
    }
    return render(request, 'blog_detail.html', context)


"""api List view   Category, Post, Comment"""
""" get all , post"""


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""single api detailed view  get,put,del"""


class CategoryDetail(APIView):
    def get(self,  *args, **kwargs):
        try:
            category = Category.objects.get(id=self.kwargs['id'])
            serializer = CategorySerializer(instance=category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        try:
            category = Category.objects.get(pk=self.kwargs['id'])
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        try:
            category = Category.objects.get(pk=self.kwargs['id'])
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            raise Http404


class PostDetail(APIView):
    def get(self, *args, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['id'])
            serializer = PostSerializer(instance=post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['id'])
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['id'])
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            raise Http404


class CommentDetail(APIView):
    def get(self, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=self.kwargs['id'])
            serializer = CommentSerializer(instance=comment)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=self.kwargs['id'])
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=self.kwargs['id'])
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise Http404
