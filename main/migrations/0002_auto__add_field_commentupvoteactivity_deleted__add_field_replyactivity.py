# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CommentUpvoteActivity.deleted'
        db.add_column(u'main_commentupvoteactivity', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ReplyActivity.deleted'
        db.add_column(u'main_replyactivity', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'PostUpvoteActivity.deleted'
        db.add_column(u'main_postupvoteactivity', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CommentMentionActivity.deleted'
        db.add_column(u'main_commentmentionactivity', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Vote.deleted'
        db.add_column(u'main_vote', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CommentVote.deleted'
        db.add_column(u'main_commentvote', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CommentUpvoteActivity.deleted'
        db.delete_column(u'main_commentupvoteactivity', 'deleted')

        # Deleting field 'ReplyActivity.deleted'
        db.delete_column(u'main_replyactivity', 'deleted')

        # Deleting field 'PostUpvoteActivity.deleted'
        db.delete_column(u'main_postupvoteactivity', 'deleted')

        # Deleting field 'CommentMentionActivity.deleted'
        db.delete_column(u'main_commentmentionactivity', 'deleted')

        # Deleting field 'Vote.deleted'
        db.delete_column(u'main_vote', 'deleted')

        # Deleting field 'CommentVote.deleted'
        db.delete_column(u'main_commentvote', 'deleted')


    models = {
        u'main.activity': {
            'Meta': {'object_name': 'Activity'},
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            'date_pub': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']", 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.commentmentionactivity': {
            'Meta': {'object_name': 'CommentMentionActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'main.commentupvoteactivity': {
            'Meta': {'object_name': 'CommentUpvoteActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'main.commentvote': {
            'Meta': {'object_name': 'CommentVote'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.googler': {
            'Meta': {'object_name': 'Googler'},
            'color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.post': {
            'Meta': {'object_name': 'Post'},
            'date_pub': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'score': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.postupvoteactivity': {
            'Meta': {'object_name': 'PostUpvoteActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']"})
        },
        u'main.replyactivity': {
            'Meta': {'object_name': 'ReplyActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Post']", 'null': 'True', 'blank': 'True'})
        },
        u'main.upvoteactivity': {
            'Meta': {'object_name': 'UpvoteActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'main.vote': {
            'Meta': {'object_name': 'Vote'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['main']