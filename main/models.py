from django.db import models
from django.db.models import Model, ForeignKey, TextField, BooleanField, \
    SmallIntegerField, ManyToManyField, CharField, BigIntegerField, \
    DateTimeField
import json
import datetime
import math
import re
from django.utils import timezone

from main.temp import user

def pick(d, keys):
    result = {}
    
    for key in keys:
        result[key] = d[key]
    
    return result

def get_object_or(M, default, *args, **keywords):
    try:
        return M.objects.get(*args, **keywords)
    except M.DoesNotExist:
        return default

def get_object_attr_or(M, attr, default, *args, **keywords):
    try:
        return M.objects.get(*args, **keywords).__getattribute__(attr)
    except M.DoesNotExist:
        return default

def ms_since_epoch(dt):
    if timezone.is_aware(dt): 
        dt = timezone.localtime(dt)
    
    epoch = \
        datetime.datetime(1970, 1, 1, tzinfo = timezone.get_current_timezone())
    
    return int((dt - epoch).total_seconds())

class JSONable():
    def as_json_dict(self):
        return pick(self.__dict__, self.json_keys())
    
    def as_json(self):
        return json.dumps(self.as_json_dict())
    
    @staticmethod
    def all_as_json(objs):
        return '[' + ', '.join(map((lambda obj: obj.as_json()), objs)) + ']'

class Post(Model, JSONable):
    username = CharField(max_length = 255)
    title = TextField()
    link = TextField(blank = True)
    text = TextField(blank = True)
    score = BigIntegerField(default = 0)
    date_pub = DateTimeField(auto_now_add = True)
    deleted = BooleanField(default = False)
    
    def json_keys(self):
        return ['id', 'title', 'text', 'link', 'score', 'username']
    
    def soft_delete(self):
        for comment in self.comment_set.all():
            comment.soft_delete()
        self.deleted = True
        self.save()
    
    def as_json_dict(self):
        d = super(Post, self).as_json_dict()
        d['mark'] = get_object_attr_or(
            Vote,
            'mark',
            0, 
            post = self, 
            username = user.nickname())
        d['timestamp'] = ms_since_epoch(self.date_pub)
        return d
    
    def as_full_json_dict(self):
        d = self.as_json_dict()
        d['color'] = Googler.color_of(user.nickname())
        return d
    
    def as_summary_json_dict(self):
        d = self.as_json_dict()
        d.pop('text')
        return d
    
    def __vote__(self, mark):
        votes = Vote.objects.filter(username = user.nickname(), post = self)
        if 0 < votes.count():
            vote = votes[0]
            vote.mark = mark
            vote.save()
        else:
            Vote.objects.create(
                username = user.nickname(),
                post = self,
                mark = mark)

    def upvote(self):
        self.__vote__(1)
    
    def downvote(self):
        self.__vote__(-1)
    
    def unvote(self):
        self.__vote__(0)
    
    def refresh_score(self):
        score = 0
        for vote in self.vote_set.all(): 
            score += vote.mark
        self.score = score
        self.save()
        return self
    
    def hottest_rank(self):
        K = 1e9
        self.refresh_score()
        if 0 <= self.score:
            return (0, - ms_since_epoch(self.date_pub) - \
                K * math.log(self.score + 1))
        else:
            return (1, - self.score)
    
    @staticmethod
    def hottest(start = False, maximum = False):
        posts = list(Post.objects.all())
        then = timezone.now()
        posts.sort(key = lambda post: post.hottest_rank())
        
        if start:
            posts = posts[start:]
        
        if maximum:
            posts = posts[:maximum]
        
        return posts
    
    @staticmethod
    def latest(start = False, maximum = False):
        posts = Post.objects.order_by('-date_pub')
        
        if start:
            posts = posts[start:]
        
        if maximum:
            posts = posts[:maximum]
        
        return list(posts)
    
    @staticmethod
    def is_valid_link(str):
        go_link_pattern = re.compile('^go/[^ ]*$')
        is_go_link = None != go_link_pattern.search(str)
        is_http_url = None != URLValidator().regex.search(str)
        return is_http_url or is_go_link


class Activity(Model, JSONable):
    sender = CharField(max_length = 255)
    receiver = CharField(max_length = 255)
    read = BooleanField(default = False)
    comment = ForeignKey('Comment')
    date_sent = DateTimeField(auto_now_add = True)

    def json_keys(self):
        return ['sender', 'receiver', 'read']

class Comment(Model, JSONable):
    username = CharField(max_length = 255)
    text = TextField(blank = True)
    post = ForeignKey(Post, blank = True, null = True)
    parent_comment = ForeignKey('Comment', blank = True, null = True)
    score = BigIntegerField(default = 0)
    date_pub = DateTimeField(auto_now_add = True)
    deleted = BooleanField(default = False)
    
    def json_keys(self):
        return ['id', 'text', 'score', 'username', 'deleted']
    
    def as_json_dict(self):
        self.refresh_score()
        d = super(Comment, self).as_json_dict()
        d['mark'] = get_object_attr_or(
            CommentVote,
            'mark',
            0,
            comment = self,
            username = user.nickname())
        d['timestamp'] = ms_since_epoch(self.date_pub)
        return d
    
    def as_tree_of_json_dicts(self):
        tree = self.__as_tree_of_json_dicts_helper__({})
        
        Comment.pop_deleted_children(tree['children'])
        
        return tree
    
    def __as_tree_of_json_dicts_helper__(self, stringified):
        if stringified.has_key(self.id):
            raise RuntimeError(
                'Circular Reference! I saw this twice: ' + \
                self.as_json() + ' ' + ' ' + str(stringified))
        else:
            d = self.as_json_dict()
            stringified[self.id] = stringified.copy()
            map(
                lambda comment: comment.refresh_score(),
                self.comment_set.all())
            d['children'] = map(
                lambda comment: 
                    comment.__as_tree_of_json_dicts_helper__(stringified),
                self.comment_set.order_by('score').all())
            return d
    
    def as_tree_of_json(self):
        return json.dumps(self.as_tree_of_json_dicts())
    
    def __vote__(self, mark):
        votes = CommentVote.objects.\
            filter(username = user.nickname(), comment = self)
        if 0 < votes.count():
            vote = votes[0]
            vote.mark = mark
            vote.save()
        else:
            CommentVote.objects.create(
                username = user.nickname(),
                comment = self,
                mark = mark)

    def upvote(self):
        self.__vote__(1)
    
    def downvote(self):
        self.__vote__(-1)
    
    def unvote(self):
        self.__vote__(0)
    
    def refresh_score(self):
        score = 0
        for vote in self.commentvote_set.all(): 
            score += vote.mark
        self.score = score
        self.save()
        return self
    
    def soft_delete(self):
        self.deleted = True
        self.save()
    
    def gen_activities(self):
        username_pattern = re.compile('(?<=@)[A-Za-z0-9_]+')
        for username in set(username_pattern.findall(self.text)):
            Activity.objects.create(
                sender = user.nickname(),
                receiver = username,
                comment = self)
    
    @staticmethod
    def pop_deleted_children(children):
        for child in children:
            map(Comment.pop_deleted_children, child['children'])
            if child['deleted'] and 0 == len(child['children']):
                children.remove(child)

class Tag(Model):
    name = TextField()
    posts = ManyToManyField(Post, blank = True, null = True)

class Vote(Model):
    username = CharField(max_length = 255)
    post = ForeignKey(Post)
    mark = SmallIntegerField(default = 0)

class CommentVote(Model):
    username = CharField(max_length = 255)
    comment = ForeignKey(Comment)
    mark = SmallIntegerField(default = 0)

class Googler(Model):
    username = CharField(max_length = 255)
    color = CharField(max_length = 255)
    
    @staticmethod
    def color_of(username):
        return get_object_attr_or(Googler, 'color', '', username = username)
