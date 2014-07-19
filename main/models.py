from django.db import models
from django.db.models import Model, ForeignKey, TextField, BooleanField, \
    SmallIntegerField, ManyToManyField, CharField, BigIntegerField, \
    DateTimeField
import json
import datetime
import math
import re
from django.utils import timezone

from main.googler import nickname

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

def mentions(text):
    username_pattern = re.compile('(?<=@)[A-Za-z0-9_]+')
    return set(username_pattern.findall(text))

class JSONable():
    def as_json_dict(self):
        return pick(self.__dict__, self.json_keys())
    
    def as_json(self):
        return json.dumps(self.as_json_dict())
    
    @staticmethod
    def all_as_json(objs):
        return '[' + ', '.join(map((lambda obj: obj.as_json()), objs)) + ']'
    
    @staticmethod
    def all_as_json_dict(objs):
        return [obj.as_json_dict() for obj in objs]

class Deletable():
    def soft_delete(self):
        self.deleted = True
        self.save()
    
    @classmethod
    def not_deleted(cls):
        return cls.objects.filter(deleted = False)

class Post(Model, JSONable, Deletable):
    username = CharField(max_length = 255)
    title = TextField()
    link = TextField(blank = True)
    text = TextField(blank = True)
    score = BigIntegerField(default = 0)
    date_pub = DateTimeField(auto_now_add = True)
    deleted = BooleanField(default = False)
    
    def __unicode__(self):
        return ('(deleted)' if self.deleted else '') + \
            'username = ' + self.username 
    
    def json_keys(self):
        return ['id', 'title', 'text', 'link', 'score', 'username', 'deleted']
    
    def soft_delete(self):
        super(Post, self).soft_delete()
        
        things = \
            list(self.comment_set.all()) + \
            list(self.postupvoteactivity_set.all()) + \
            list(self.vote_set.all())
        
        for thing in things:
            thing.soft_delete()
        
    def as_json_dict(self):
        d = super(Post, self).as_json_dict()
        d['mark'] = get_object_attr_or(
            Vote,
            'mark',
            0, 
            post = self, 
            username = nickname())
        d['timestamp'] = ms_since_epoch(self.date_pub)
        return d
    
    def as_full_json_dict(self):
        d = self.as_json_dict()
        d['color'] = Googler.current().color
        return d
    
    def as_summary_json_dict(self):
        d = self.as_json_dict()
        d.pop('text')
        return d
    
    def __vote__(self, mark):
        votes = Vote.objects.filter(username = nickname(), post = self)
        if 0 < votes.count():
            vote = votes[0]
            vote.mark = mark
            vote.save()
        else:
            vote = Vote.objects.create(
                username = nickname(),
                post = self,
                mark = mark)
        
        vote.gen_activity()

    def upvote(self):
        self.__vote__(Googler.current().get_vote())
    
    def downvote(self):
        self.__vote__(- Googler.current().get_vote())
    
    def unvote(self):
        self.__vote__(0)
    
    def refresh_score(self):
        score = 0
        for vote in self.vote_set.all(): 
            score += vote.mark
        self.score = score
        self.save()
        return self
    
    def clean(self):
        self.refresh_score()
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
        posts = list(Post.not_deleted())
        then = timezone.now()
        posts.sort(key = lambda post: post.hottest_rank())
        
        if start:
            posts = posts[start:]
        
        if maximum:
            posts = posts[:maximum]
        
        return posts
    
    @staticmethod
    def latest(start = False, maximum = False):
        posts = Post.not_deleted().order_by('-date_pub')
        
        if start:
            posts = posts[start:]
        
        if maximum:
            posts = posts[:maximum]
        
        return list(posts)
    
    @staticmethod
    def is_valid_link(str):
        http_url_pattern = r'^(?:(?:http|https)://)?(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)(?::\d+)?(?:/?|[/?]\S+)$'
        go_link_pattern = re.compile('^go/[^ ]*$')
        is_go_link = None != go_link_pattern.search(str)
        is_http_url = None != http_url_pattern.search(str)
        return is_http_url or is_go_link

class Comment(Model, JSONable, Deletable):
    username = CharField(max_length = 255)
    text = TextField(blank = True)
    post = ForeignKey(Post, blank = True, null = True)
    parent_comment = ForeignKey('Comment', blank = True, null = True)
    score = BigIntegerField(default = 0)
    date_pub = DateTimeField(auto_now_add = True)
    deleted = BooleanField(default = False)
    
    def get_parent(self):
        return self.post or self.parent_comment
    
    def get_post(self):
        return self.post or self.parent_comment.get_post()
    
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
            username = nickname())
        d['timestamp'] = ms_since_epoch(self.date_pub)
        return d
    
    def as_tree_of_json_dicts(self):
        tree = self.__as_tree_of_json_dicts_helper__({})
        
        # Comment.pop_deleted_children(tree['children'])
        
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
            d['childs'] = map(
                lambda comment: 
                    comment.__as_tree_of_json_dicts_helper__(stringified),
                self.comment_set.order_by('score').all())
            return d
    
    def as_tree_of_json(self):
        return json.dumps(self.as_tree_of_json_dicts())
    
    def __vote__(self, mark):
        votes = CommentVote.objects.\
            filter(username = nickname(), comment = self)
        if 0 < votes.count():
            vote = votes[0]
            vote.mark = mark
            vote.save()
        else:
            vote = CommentVote.objects.create(
                username = nickname(),
                comment = self,
                mark = mark)
        
        vote.gen_activity()

    def upvote(self):
        self.__vote__(Googler.current().get_vote())
    
    def downvote(self):
        self.__vote__(- Googler.current().get_vote())
    
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
        super(Comment, self).soft_delete()
        
        things = \
            list(self.commentupvoteactivity_set.all()) + \
            list(self.commentmentionactivity_set.all()) + \
            list(self.replyactivity_set.all()) + \
            list(self.commentvote_set.all())
        
        for thing in things:
            thing.soft_delete()
        
        self.deleted = True
        self.save()
    
    def gen_mention_activities(self):
        for username in mentions(self.text):
            if username != self.username:
                CommentMentionActivity.objects.get_or_create(
                    sender = self.username,
                    receiver = username,
                    comment = self)
    
    def gen_reply_activity(self):
        if self.username != self.get_parent().username:
            ReplyActivity.objects.get_or_create(
                sender = self.username,
                receiver = self.get_parent().username,
                comment = self)
    
    @staticmethod
    def pop_deleted_children(children):
        for child in children:
            map(Comment.pop_deleted_children, child['children'])
            if child['deleted'] and 0 == len(child['children']):
                children.remove(child)

class Activity(Model, JSONable):
    sender = CharField(max_length = 255)
    receiver = CharField(max_length = 255)
    read = BooleanField(default = False)
    date_sent = DateTimeField(auto_now_add = True)

    def json_keys(self):
        return ['sender', 'receiver', 'read']
    
    @staticmethod
    def all_objects():
        subclasses = [
            PostUpvoteActivity,
            CommentUpvoteActivity,
            CommentMentionActivity,
            ReplyActivity,
        ]
        
        activities = []        
        for subclass in subclasses:
            activities += subclass.objects.all()
        
        return activities

class UpvoteActivity(Activity):
    pass

class PostUpvoteActivity(Activity, Deletable):
    post = ForeignKey(Post)
    deleted = BooleanField(default = False)
    
    def as_json_dict(self):
        return {
            'type': 'post like',
            'sender': self.sender,
            'post_id': self.post.id,
            'title': self.post.title,
            'read': self.read,
        }

class CommentUpvoteActivity(Activity, Deletable):
    comment = ForeignKey(Comment)
    deleted = BooleanField(default = False)
    
    def as_json_dict(self):
        return {
            'type': 'comment like',
            'sender': self.sender,
            'comment_id': self.comment.id,
            'read': self.read,
        }

class CommentMentionActivity(Activity, Deletable):
    comment = ForeignKey(Comment)
    deleted = BooleanField(default = False)
    
    def as_json_dict(self):
        return {
            'type': 'mention in comment',
            'sender': self.sender,
            'comment_id': self.comment.id,
            'post_id': self.comment.get_post().id,
            'text': self.comment.text,
            'read': self.read,
        }

class ReplyActivity(Activity, Deletable):
    comment = ForeignKey(Comment)
    deleted = BooleanField(default = False)
    
    def as_json_dict(self):
        return {
            'type': 'reply',
            'sender': self.sender,
            'comment_id': self.comment.id,
            'post_id': self.comment.get_post().id,
            'text': self.comment.text,
            'read': self.read,
        }

class Tag(Model):
    name = TextField()
    posts = ManyToManyField(Post, blank = True, null = True)

class Vote(Model, Deletable):
    username = CharField(max_length = 255)
    post = ForeignKey(Post)
    mark = SmallIntegerField(default = 0)
    deleted = BooleanField(default = False)
    
    def gen_activity(self):
        if self.mark == 1 and self.username != self.post.username:
            PostUpvoteActivity.objects.get_or_create(
                sender = self.username,
                receiver = self.post.username,
                post = self.post)

class CommentVote(Model, Deletable):
    username = CharField(max_length = 255)
    comment = ForeignKey(Comment)
    mark = SmallIntegerField(default = 0)
    deleted = BooleanField(default = False)
    
    def gen_activity(self):
        if self.mark == 1 and self.username != self.comment.username:
            CommentUpvoteActivity.objects.get_or_create(
                sender = self.username,
                receiver = self.comment.username,
                post = self.comment)

class Googler(Model):
    username = CharField(max_length = 255)
    color = CharField(max_length = 255, default = '')
    
    SPECIAL_USERNAMES = [
        'tennien',
        'soturntup',
    ]
    SPECIAL_VOTE = 2
    
    def __unicode__(self):
        return self.username
    
    def get_vote(self, username):
        if Googler.named(username).is_special():
            return Googler.SPECIAL_VOTE
        else:
            return 1
    
    def is_special(self):
        return self.username in Googler.SPECIAL_USERNAMES
    
    @staticmethod
    def named(username):
        return Googler.objects.get_or_create(username = username)[0]
    
    @staticmethod
    def current():
        return Googler.named(nickname())
    
    @staticmethod
    def current_is_special(username):
        return Googler.is_special(nickname())
