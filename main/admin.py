from django.contrib import admin
import main.models

admin.site.register(main.models.Comment)
admin.site.register(main.models.CommentMentionActivity)
admin.site.register(main.models.CommentUpvoteActivity)
admin.site.register(main.models.CommentVote)
admin.site.register(main.models.Googler)
admin.site.register(main.models.Post)
admin.site.register(main.models.PostUpvoteActivity)
admin.site.register(main.models.ReplyActivity)
admin.site.register(main.models.Tag)
admin.site.register(main.models.UpvoteActivity)
admin.site.register(main.models.Vote)
