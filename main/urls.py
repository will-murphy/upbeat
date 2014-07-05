from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^$', views.root),
    url(r'^post/create$', views.post_create),
    url(r'^post/([^/]+?)/upvote$', views.post_upvote),
    url(r'^post/([^/]+?)/downvote$', views.post_downvote),
    url(r'^post/([^/]+?)/json$', views.post_json),
    url(r'^post/comments_page$', views.post_comments_page),
    url(r'^post/by/([^/]+?)$', views.post_by),
    url(r'^comment/([^/]+?)/json$', views.comment_json),
    url(r'^comment/([^/]+?)/tree$', views.comment_tree),
    url(r'^comment/create$', views.comment_create),
    url(r'^comment/([^/]+?)/upvote$', views.comment_upvote),
    url(r'^comment/([^/]+?)/downvote$', views.comment_downvote),
    url(r'^activity/how-many-unread$', views.activity_how_many_unread),
    url(r'^activity/recent$', views.activity_recent),
)
