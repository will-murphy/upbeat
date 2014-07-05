from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from main.models import Post, Comment, Activity
import json

# from google.appengine.api import users
# user = users.get_current_users()
from main.temp import user

def respond(str, data = {}):
    return HttpResponse(json.dumps(dict(
        data.items() + \
        {'message': str}.items())))

def root(request):
    return render(request, 'main/home.html', {})

def post_create(request):
    post = Post(
        username = user.nickname(),
        title = request.POST['title'],
        link = request.POST.get('link', False),
        text = request.POST.get('text', False))
    post.save()
    return respond('Saved post.')

def post_upvote(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.upvote()
    return respond('Upvoted post.')

def post_downvote(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.downvote()
    return respond('Downvoted post.')

def post_json(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return HttpResponse(post.as_json())

def post_comments_page(request):
    return render(request, 'main/comments_page.html', {})

def post_by(request):
    return Post.all_as_json(Post.object.get(
        username = request.GET.get('username')))

def comment_json(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    return HttpResponse(comment.as_json())

def comment_tree(request):
    return HttpResponse(comment.tree_as_json())

def comment_create(request):
    comment = Comment(
        username = user.nickname(),
        title = request.POST['title'],
        link = request.POST.get('link', False),
        text = request.POST.get('text', False))
    comment.save()
    return respond('Saved comment.')

def comment_upvote(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.upvote()
    return respond('Upvoted comment.')

def comment_downvote(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.downvote()
    return respond('Downvoted comment.')

def activity_how_many_unread(request):
    unread = Activity.objects.filter(
        read = False, 
        reciever = request.GET.get('reciever'))
    count = unread.count()
    return HttpResponse(json.dumps(count))

def activity_recent(request):
    results = Activity.objects.\
        filter(reciever = request.GET.get('receiver')).\
        order_by('-date_sent')\
        [:int(request.GET.get('count'))]
    return HttpResponse(Comment.all_as_json(list(results)))
