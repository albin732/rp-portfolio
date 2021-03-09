from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category"),

    path('category_api', views.CategoryList.as_view()),
    path('post_api', views.PostList.as_view(), name='post_api'),
    path('comment_api', views.CommentList.as_view()),

    path('category_api/<int:id>/', views.CategoryDetail.as_view()),
    path('post_api/<int:id>/', views.PostDetail.as_view()),
    path('comment_api/<int:id>/', views.CommentDetail.as_view()),
]
