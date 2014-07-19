from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponsePermanentRedirect
from main.models import Post, Comment, Activity, Vote, CommentVote, Googler, \
    get_object_or, SPECIAL_USERS
import json
import re

from main.googler import get_current_user, nickname

def respond(str, data = {}):
    return HttpResponse(json.dumps(dict(
        data.items() + \
        {'message': str}.items())))

def root(request):
    # from google.appengine.api import users
    return render(request, 'main/index.html', {
        'title': 'Hottest',
        'listtype': 'hottest',
        'inuser': nickname()
        })

def latest(request):
    return render(request, 'main/index.html', {
        'title': 'Latest',
        'listtype': 'latest',
        'inuser': nickname()
        })

def user_page(request, username):
    return render(request, 'main/index.html', {
        'title': username.capitalize() + "'s Profile",
        'listtype': 'user|' + username,
        'inuser': nickname(),
        'color': Googler.color_of(username),
        'username': username,
        'Username': username.capitalize(),
        'specialuser': username in SPECIAL_USERS
        })

def notifications_page(request):
    return render(request, 'main/notifications.html', {
        'inuser': nickname()
        })

def post_hottest(request):
    posts = list(Post.hottest(
        request.GET.get('start', 0),
        request.GET.get('max', 150)))
    
    for post in posts: post.refresh_score()
    
    posts = filter(lambda post: False == post.deleted, posts)
    
    return HttpResponse(json.dumps({'posts': map(
        lambda post: post.as_summary_json_dict(), 
        posts)}))

def post_latest(request):
    posts = list(Post.latest(
        request.GET.get('start', 0),
        request.GET.get('max', 150)))
    
    for post in posts: post.refresh_score()
    
    posts = filter(lambda post: False == post.deleted, posts)
    
    return HttpResponse(json.dumps({'posts': map(
        lambda post: post.as_summary_json_dict(),
        posts)}))

def post_create(request):
    post = Post.objects.create(
        username = nickname(),
        title = request.POST['title'],
        link = request.POST.get('link', ['']),
        text = request.POST.get('text', ['']))
    post.save()
    post.upvote()
    return respond('Saved post.', {'id': post.id})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk = pk)
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
    
    post.refresh_score()
    result['post'] = post.as_full_json_dict()
    
    for comment in post.comment_set.all(): comment.refresh_score()
    
    result['comments'] = map(
        lambda comment: comment.as_tree_of_json_dicts(),
        post.comment_set.order_by('-score').all())
    
    return HttpResponse(json.dumps(result))

def post_comments_page(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    
    post.refresh_score()
    
    if post.deleted: 
        return render(request, 'main/post-deleted.html', {
            'post': post.as_json_dict(),
            'inuser': nickname(),
            'color': Googler.color_of(post.username)
            })
    
    return render(request, 'main/comments.html', {
        'post': post.as_json_dict(),
        'inuser': nickname(),
        'color': Googler.color_of(post.username)
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
    post = get_object_or(
        Post, 
        None, 
        id = request.POST.get('post_id', None))
    
    parent_comment = get_object_or(
        Comment,
        None,
        id = request.POST.get('parent_comment_id', None))
    
    if parent_comment: post = None
    
    comment = Comment.objects.create(
        username = nickname(),
        text = request.POST.get('text', ''),
        post = post,
        parent_comment = parent_comment)
    
    comment.gen_mention_activities()
    comment.gen_reply_activity()
    comment.upvote()
    return respond('Saved comment.', {'id': comment.id})

def comment_update(request):
    comment = get_object_or_404(Comment, id = request.POST['id'])
    comment.text = request.POST.get('text', comment.text)
    comment.save()
    return respond('Updated comment.')

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id = pk)
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
        receiver = nickname())
    count = unread.count()
    return HttpResponse(json.dumps(count))

def activity_recent(request):
    results = Activity.objects.\
        filter(receiver = nickname()).\
        order_by('-date_sent')
    
    if request.GET.has_key('max'):
        results = results[:int(request.GET['max'])]
    
    return HttpResponse(Activity.all_as_json(list(results)))

def activity_own(request):
    
    # Get the activities.
    
    activities = filter(
        lambda activity: activity.receiver == nickname(), 
        Activity.all_objects())
    
    activities = map(
        lambda activity: activity.as_json_dict(),
        activities)
    
    if 0 == len(activities):
        response = {'No': []}
    else:
        response = {
            'Unread': filter(
                lambda activity: activity['read'] == False,
                activities), 
            'Old': filter(lambda activity: activity['read'] == True,
                activities)[:20]
        }
    
    # Read all unreads.
    
    unreads = filter(
        lambda activity: \
            activity.receiver == nickname() and \
            activity.read == False,
        Activity.all_objects())
    
    for unread in unreads:
        unread.read = True
        unread.save()
    
    # Return the activities.
    
    return HttpResponse(json.dumps(response))

def user_page_json(request, username):
    posts = Post.not_deleted().\
        filter(username = username).\
        order_by('-date_pub')\
        [:100]
    
    for post in posts: post.refresh_score()
    
    response = {
        'userinfo': {
            'posts': posts.count(),
            'color': Googler.color_of(username),
        },
        'posts': [post.as_summary_json_dict() for post in posts.all()]
    }
    
    return HttpResponse(json.dumps(response))

def user_set_color(request):
    googler, created = Googler.objects.get_or_create(username = nickname())
    googler.color = request.POST.get('color', '')
    googler.save()
    return respond('Set ' + googler.username + '\'s color to ' + googler.color + '.')

def unshorten(request):
    return HttpResponsePermanentRedirect(
        '/comments/' + request.META['QUERY_STRING'])
