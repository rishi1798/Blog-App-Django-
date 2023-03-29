from django.urls import path
from . import views

urlpatterns = [
    path("",views.StartingPage.as_view(),name="starting-page"),
    path("posts/",views.AllPosts.as_view(),name="posts-page"),
    path("posts/<slug:slug>",views.DetailPosts.as_view(),name="post-detail-page"),
    path("liked/<slug:slug>",views.liked,name="liked-post"),
    path("unliked/<slug:slug>",views.unliked,name="unliked-post"),
    path("read-later/",views.ReadLaterView.as_view(),name="read-later"),
    path("create-post/",views.create_post,name="create-post")
]
