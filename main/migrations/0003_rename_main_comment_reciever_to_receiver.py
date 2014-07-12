# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Comment.date_pub'
        db.rename_column(u'main_activity', 'reciever', 'receiver')


    def backwards(self, orm):
        db.rename_column(u'main_activity', 'receiver', 'reciever')