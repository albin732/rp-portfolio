from django.shortcuts import render
from blog.models import Post, Comment, Category
from .forms import CommentForm

from . serializers import CategorySerializer, PostSerializer, CommentSerializer
from rest_framework.response import Response

from rest_framework.views import APIView


# Create your views here.


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


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get(self,  *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['id'])
        serializer = CategorySerializer(instance=category)
        return Response(serializer.data)


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetail(APIView):
    def get(self, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['id'])
        serializer = PostSerializer(instance=post)
        return Response(serializer.data)


class CommentList(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentDetail(APIView):
    def get(self, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['id'])
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data)
