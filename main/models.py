from django.db import models
from django.db.models import Model, ForeignKey, TextField, BooleanField, \
    SmallIntegerField, ManyToManyField, CharField, BigIntegerField, \
    DateTimeField
import json

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
        return '[' + ', '.join(map((lambda obj: obj.as_json), objs)) + ']'

class Post(Model, JSONable):
    username = CharField(max_length = 255)
    title = TextField()
    link = TextField()
    text = TextField()
    score = BigIntegerField(default = 0)
    
    def json_keys(self):
        return ['username', 'title', 'link', 'text', 'score']

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
    
    def as_tree_of_dicts(self, stringified = {}):
        if stringified.has_key(self):
            raise RuntimeError(
                'Circular Reference! I saw this twice:' + \
                self.as_json())
        else:
            d = self.as_dict()
            d[self] = True
            d['comment_set'] = self.comment_set.map(
                lambda comment: comment.tree_as_json(stringified))
            return d
    
    def as_tree_of_json(self):
        return json.dumps(self.as_tree_of_dicts())

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
