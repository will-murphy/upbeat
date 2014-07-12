# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table(u'main_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('score', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('date_pub', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['Post'])

        # Adding model 'Comment'
        db.create_table(u'main_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Post'], null=True, blank=True)),
            ('parent_comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'], null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('date_pub', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['Comment'])

        # Adding model 'Activity'
        db.create_table(u'main_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('receiver', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Activity'])

        # Adding model 'UpvoteActivity'
        db.create_table(u'main_upvoteactivity', (
            (u'activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Activity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'main', ['UpvoteActivity'])

        # Adding model 'PostUpvoteActivity'
        db.create_table(u'main_postupvoteactivity', (
            (u'activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Activity'], unique=True, primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Post'])),
        ))
        db.send_create_signal(u'main', ['PostUpvoteActivity'])

        # Adding model 'CommentUpvoteActivity'
        db.create_table(u'main_commentupvoteactivity', (
            (u'activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Activity'], unique=True, primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
        ))
        db.send_create_signal(u'main', ['CommentUpvoteActivity'])

        # Adding model 'CommentMentionActivity'
        db.create_table(u'main_commentmentionactivity', (
            (u'activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Activity'], unique=True, primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
        ))
        db.send_create_signal(u'main', ['CommentMentionActivity'])

        # Adding model 'ReplyActivity'
        db.create_table(u'main_replyactivity', (
            (u'activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Activity'], unique=True, primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
        ))
        db.send_create_signal(u'main', ['ReplyActivity'])

        # Adding model 'Tag'
        db.create_table(u'main_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Tag'])

        # Adding M2M table for field posts on 'Tag'
        m2m_table_name = db.shorten_name(u'main_tag_posts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm[u'main.tag'], null=False)),
            ('post', models.ForeignKey(orm[u'main.post'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'post_id'])

        # Adding model 'Vote'
        db.create_table(u'main_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Post'])),
            ('mark', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['Vote'])

        # Adding model 'CommentVote'
        db.create_table(u'main_commentvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
            ('mark', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['CommentVote'])

        # Adding model 'Googler'
        db.create_table(u'main_googler', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('color', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal(u'main', ['Googler'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table(u'main_post')

        # Deleting model 'Comment'
        db.delete_table(u'main_comment')

        # Deleting model 'Activity'
        db.delete_table(u'main_activity')

        # Deleting model 'UpvoteActivity'
        db.delete_table(u'main_upvoteactivity')

        # Deleting model 'PostUpvoteActivity'
        db.delete_table(u'main_postupvoteactivity')

        # Deleting model 'CommentUpvoteActivity'
        db.delete_table(u'main_commentupvoteactivity')

        # Deleting model 'CommentMentionActivity'
        db.delete_table(u'main_commentmentionactivity')

        # Deleting model 'ReplyActivity'
        db.delete_table(u'main_replyactivity')

        # Deleting model 'Tag'
        db.delete_table(u'main_tag')

        # Removing M2M table for field posts on 'Tag'
        db.delete_table(db.shorten_name(u'main_tag_posts'))

        # Deleting model 'Vote'
        db.delete_table(u'main_vote')

        # Deleting model 'CommentVote'
        db.delete_table(u'main_commentvote')

        # Deleting model 'Googler'
        db.delete_table(u'main_googler')


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
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"})
        },
        u'main.commentupvoteactivity': {
            'Meta': {'object_name': 'CommentUpvoteActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"})
        },
        u'main.commentvote': {
            'Meta': {'object_name': 'CommentVote'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
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
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']"})
        },
        u'main.replyactivity': {
            'Meta': {'object_name': 'ReplyActivity', '_ormbases': [u'main.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['main']