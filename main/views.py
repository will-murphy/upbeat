from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from main.models import Post, Comment, Activity, Vote, CommentVote
import json

# from google.appengine.api import users
# user = users.get_current_users()
from main.temp import user

def respond(str, data = {}):
    return HttpResponse(json.dumps(dict(
        data.items() + \
        {'message': str}.items())))

def root(request):
    return render(request, 'main/home.html', {'listtype': 'hottest'})

def latest(request):
    return render(request, 'main/home.html', {'listtype': 'latest'})

def user_page(request, username):
    return render(request, 'main/home.html', {
        'listtype': 'user|' + username
        })

def post_hottest(request):
    posts = Post.hottest(
        request.GET.get('start', 0),
        request.GET.get('max', None))
    return HttpResponse(Post.all_as_json(posts))

def post_latest(request):
    posts = Post.latest(
        request.GET.get('start', 0),
        request.GET.get('max', None))
    return HttpResponse(Post.all_as_json(posts))

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
    post.refresh_score()
    return HttpResponse(post.as_json())

def post_comments_page(request, post_id):
    return render(request, 'main/comments_page.html', {})

def post_by(request, username):
    return HttpResponse(Post.all_as_json(map(
        lambda post: post.refresh_score(),
        Post.objects.filter(username = username).all())))

def comment_json(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    return HttpResponse(comment.as_json())

def comment_tree(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    return HttpResponse(comment.as_tree_of_json())

def comment_create(request):
    comment = Comment(
        username = user.nickname(),
        text = request.POST.get('text', False),
        post = Post.objects.get(request.POST.get('post_id', False), None),
        parent_comment = Post.objects.get(
            request.POST.get('parent_comment_id', False),
            None))
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
        reciever = request.GET.get('receiver'))
    count = unread.count()
    return HttpResponse(json.dumps(count))

def activity_recent(request):
    results = Activity.objects.\
        filter(reciever = request.GET['receiver']).\
        order_by('-date_sent')
    if request.GET.has_key('max'):
        results = results[:int(request.GET['max'])]
    
    return HttpResponse(Comment.all_as_json(list(results)))
