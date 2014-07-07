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
        ))
        db.send_create_signal(u'main', ['Post'])

        # Adding model 'Activity'
        db.create_table(u'main_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reciever', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Activity'])

        # Adding model 'Comment'
        db.create_table(u'main_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Post'], null=True, blank=True)),
            ('parent_comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'], null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Comment'])

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
            ('value', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'main', ['Vote'])

        # Adding model 'CommentVote'
        db.create_table(u'main_commentvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
            ('value', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'main', ['CommentVote'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table(u'main_post')

        # Deleting model 'Activity'
        db.delete_table(u'main_activity')

        # Deleting model 'Comment'
        db.delete_table(u'main_comment')

        # Deleting model 'Tag'
        db.delete_table(u'main_tag')

        # Removing M2M table for field posts on 'Tag'
        db.delete_table(db.shorten_name(u'main_tag_posts'))

        # Deleting model 'Vote'
        db.delete_table(u'main_vote')

        # Deleting model 'CommentVote'
        db.delete_table(u'main_commentvote')


    models = {
        u'main.activity': {
            'Meta': {'object_name': 'Activity'},
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reciever': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']", 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.commentvote': {
            'Meta': {'object_name': 'CommentVote'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'main.post': {
            'Meta': {'object_name': 'Post'},
            'date_pub': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'score': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Post']", 'symmetrical': 'False'})
        },
        u'main.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Post']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['main']