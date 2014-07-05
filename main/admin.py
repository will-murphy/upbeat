from django.contrib import admin
import main.models

admin.site.register(main.models.Post)
admin.site.register(main.models.Activity)
admin.site.register(main.models.Comment)
admin.site.register(main.models.Tag)
admin.site.register(main.models.Vote)
admin.site.register(main.models.CommentVote)
