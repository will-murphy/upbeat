from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^$', views.root),
    url(r'^latest$', views.latest),
    url(r'^user/([^/]+)$', views.user_page),
    url(r'^post/([^/]+)$', views.post_comments_page),
    url(r'^api/post/hottest$', views.post_hottest),
    url(r'^api/post/latest$', views.post_latest),
    url(r'^api/post/create$', views.post_create),
    url(r'^api/post/([^/]+?)/upvote$', views.post_upvote),
    url(r'^api/post/([^/]+?)/downvote$', views.post_downvote),
    url(r'^api/post/([^/]+?)/json$', views.post_json),
    url(r'^api/post/by/([^/]+?)$', views.post_by),
    url(r'^api/comment/([^/]+?)/json$', views.comment_json),
    url(r'^api/comment/([^/]+?)/tree$', views.comment_tree),
    url(r'^api/comment/create$', views.comment_create),
    url(r'^api/comment/([^/]+?)/upvote$', views.comment_upvote),
    url(r'^api/comment/([^/]+?)/downvote$', views.comment_downvote),
    url(r'^api/activity/how-many-unread$', views.activity_how_many_unread),
    url(r'^api/activity/recent$', views.activity_recent),
)
