from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from main.models import Post, Comment, Activity, Vote, CommentVote, Googler
import json
import re

# from google.appengine.api import users
# user = users.get_current_users()
from main.temp import user

def respond(str, data = {}):
    return HttpResponse(json.dumps(dict(
        data.items() + \
        {'message': str}.items())))

def root(request):
    return render(request, 'main/index.html', {
        'listtype': 'hottest',
        'inuser': user.nickname()
        })

def latest(request):
    return render(request, 'main/index.html', {
        'listtype': 'latest',
        'inuser': user.nickname()
        })

def user_page(request, username):
    return render(request, 'main/index.html', {
        'listtype': 'user|' + username
        })

def post_hottest(request):
    posts = list(Post.hottest(
        request.GET.get('start', 0),
        request.GET.get('max', None)))
    
    for post in posts: post.refresh_score()
    
    posts = filter(lambda post: False == post.deleted, posts)
    
    return HttpResponse(json.dumps({'posts': map(
        lambda post: post.as_summary_json_dict(), 
        posts)}))

def post_latest(request):
    posts = list(Post.latest(
        request.GET.get('start', 0),
        request.GET.get('max', None)))
    
    for post in posts: post.refresh_score()
    
    posts = filter(lambda post: False == post.deleted, posts)
    
    return HttpResponse(json.dumps({'posts': map(
        lambda post: post.as_summary_json_dict(),
        posts)}))

def post_create(request):
    post = Post.objects.create(
        username = user.nickname(),
        title = request.POST['title'],
        link = request.POST.get('link', ['']),
        text = request.POST.get('text', ['']))
    post.save()
    post.upvote()
    return respond('Saved post.', {'id': post.id})

def post_delete(request):
    post = get_object_or_404(Post, pk = request.POST.get('post_id', ''))
    post.soft_delete()
    return respond('Deleted post.')

def post_upvote(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.upvote()
    return respond('Upvoted post.')

def post_downvote(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.downvote()
    return respond('Downvoted post.')

def post_unvote(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.unvote()
    return respond('Unvoted post.')

def post_page_json(request, pk):
    result = {}
    
    post = get_object_or_404(Post, pk = pk)
    
    if post.deleted:
        return render(request, 'main/post_has_been_deleted.html', {username: post.username})
    
    post.refresh_score()
    result['post'] = post.as_full_json_dict()
    
    result['comments'] = map(
        lambda comment: comment.as_tree_of_json_dicts(),
        post.comment_set.all())
    
    return HttpResponse(json.dumps(result))

def post_comments_page(request, post_id):
    return render(request, 'main/comments.html', {
        'post': get_object_or_404(Post, id = post_id).as_json_dict()
        })

def post_by(request, username):
    return HttpResponse(Post.all_as_json(map(
        lambda post: post.refresh_score(),
        Post.objects.filter(username = username, deleted = False).all())))

def comment_json(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    return HttpResponse(comment.as_json())

def comment_tree(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    return HttpResponse(comment.as_tree_of_json())

def comment_create(request):
    username_pattern = re.compile('(?<=@)[a-zA-Z0-9]+')
    
    comment = Comment(
        username = user.nickname(),
        text = request.POST.get('text', ''),
        post = Post.objects.get(request.POST.get('post_id', False), None),
        parent_comment = Post.objects.get(request.POST.get('parent_comment_id', False), None))
    
    comment.save()
    comment.gen_activities()
    return respond('Saved comment.', {id: comment.id})

def comment_update(request):
    comment = get_object_or_404(Comment, id = request.POST['comment_id'])
    comment.update(
        text = request.POST.get(text, comment.text))

def comment_delete(request):
    comment = get_object_or_404(
        Comment, 
        id = request.POST.get('comment_id', ''))
    comment.soft_delete()
    return respond('Deleted comment.')

def comment_upvote(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.upvote()
    return respond('Upvoted comment.')

def comment_downvote(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.downvote()
    return respond('Downvoted comment.')

def comment_unvote(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.unvote()
    return respond('Unvoted comment.')

def activity_how_many_unread(request):
    unread = Activity.objects.filter(
        read = False, 
        receiver = user.nickname())
    count = unread.count()
    return HttpResponse(json.dumps(count))

def activity_recent(request):
    results = Activity.objects.\
        filter(reciever = user.nickname()).\
        order_by('-date_sent')
    if request.GET.has_key('max'):
        results = results[:int(request.GET['max'])]
    
    return HttpResponse(Comment.all_as_json(list(results)))

def activity_own(request):
    activities = Activity.objects.filter(receiver = user.nickname()).all()
    
    response = map(
        lambda activity: {
            'username': activity.sender,
            'text': activity.comment.text,
            'post_id': activity.comment.post.id,
            'title': activity.comment.post.title,
        },
        activities)
    
    return HttpResponse(json.dumps(response))

def user_page_json(request, username):
    posts = Post.objects.filter(username = username)
    
    response = {
        'userinfo': {
            'posts': posts.count(),
            'color': Googler.color_of(username),
        },
        'posts': [post.as_summary_json_dict() for post in posts.all()]
    }
    
    return HttpResponse(json.dumps(response))

def user_set_color(request):
    Googler.create(
        username = user.nickname(),
        color = request.POST.get('color', ''))
