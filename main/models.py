from django.db import models
from django.db.models import Model, ForeignKey, TextField, BooleanField, \
    SmallIntegerField, ManyToManyField, CharField, BigIntegerField, \
    DateTimeField
import json

from main.temp import user

def pick(d, keys):
    result = {}
    
    for key in keys:
        result[key] = d[key]
    
    return result

class JSONable():
    def as_json(self):
        return json.dumps(self.as_dict())
    
    def as_dict(self):
        return pick(self.__dict__, self.json_keys())
    
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
    
    def json_keys(self):
        return ['username', 'title', 'link', 'text', 'score']
    
    def __vote__(self, value):
        votes = Vote.objects.filter(username = user.nickname(), post = self)
        if 0 < votes.count():
            vote = votes[0]
            vote.value = value
            vote.save()
        else:
            Vote.objects.create(
                username = user.nickname(),
                post = self,
                value = value)

    def upvote(self):
        self.__vote__(1)
    
    def downvote(self):
        self.__vote__(-1)
    
    def refresh_score(self):
        score = 0
        for vote in self.vote_set.all(): 
            score += vote.value
        self.score = score
        self.save()
        return self
        
        
        posts = Post.hottest()
    
    @staticmethod
    def hottest(start = False, maximum = False):
        K = 1e9
        posts = list(Post.objects.all())
        map(lambda post: post.refresh_score(), posts)
        then = datetime.datetime.now()
        posts.sort(lambda post: 
            K * math.log(post.score) - (then - post.date_pub).microseconds)
        
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

class Activity(Model):
    sender = CharField(max_length = 255)
    reciever = CharField(max_length = 255)
    read = BooleanField(default = False)
    text = TextField()
    date_sent = DateTimeField(auto_now_add = True)

class Comment(Model, JSONable):
    username = CharField(max_length = 255)
    text = TextField()
    post = ForeignKey(Post, blank = True, null = True)
    parent_comment = ForeignKey('Comment', blank = True, null = True)
    
    def json_keys(self):
        return ['text', 'username']
    
    def as_tree_of_dicts(self):
        return self.__as_tree_of_dicts_helper__({})
    
    def __as_tree_of_dicts_helper__(self, stringified):
        if stringified.has_key(self.id):
            raise RuntimeError(
                'Circular Reference! I saw this twice: ' + \
                self.as_json() + ' ' + ' ' + str(stringified))
        else:
            d = self.as_dict()
            stringified[self.id] = stringified.copy()
            d['comment_set'] = map(
                lambda comment: comment.__as_tree_of_dicts_helper__(stringified),
                self.comment_set.all())
            return d
    
    def as_tree_of_json(self):
        return json.dumps(self.as_tree_of_dicts())
    
    def __vote__(self, value):
        votes = CommentVote.objects.\
            filter(username = user.nickname(), comment = self)
        if 0 < votes.count():
            vote = votes[0]
            vote.value = value
            vote.save()
        else:
            CommentVote.objects.create(
                username = user.nickname(),
                comment = self,
                value = value)

    def upvote(self):
        self.__vote__(1)
    
    def downvote(self):
        self.__vote__(-1)

class Tag(Model):
    name = TextField()
    posts = ManyToManyField(Post)

class Vote(Model):
    username = CharField(max_length = 255)
    post = ForeignKey(Post)
    value = SmallIntegerField()

class CommentVote(Model):
    username = CharField(max_length = 255)
    comment = ForeignKey(Comment)
    value = SmallIntegerField()
