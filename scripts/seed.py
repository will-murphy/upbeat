import main.models

def delete_all(name):
    for obj in main.models.Post.objects.all(): obj.delete()

def run():
    for name in ['Post', 'Tag', 'Comment', 'Activity']: delete_all(name)
    
    post1 = main.models.Post.objects.create(
        username = 'page',
        title = 'Ding Dong Facebook is Dead.',
        text = 'Today I received a report that Facebook was found dead at 11 years old. The company is beleived to have suffered heart failure induced by an overdose of caffiene and ethanol combined with schizophrenic tendencies and extreme megalomania. We are launching a new product Google Bookface, which will replace the existing Google+.')

    post2 = main.models.Post.objects.create(
        username = 'page',
        title = 'One Google Program',
        text = 'After the recent collapse of Facebook and rise to prominance of Google Bookface, I am pleased to announce that we have partnered with the US Government in instanting the One Google program by which all children will be required at birth to create a Bookface account and friend their nearest family members. We have also dissolved the US Congress and are in the final stages of acquiring the United Nations.')

    post3 = main.models.Post.objects.create(
        username = 'penguin',
        title = 'Penguin Penguin Penguin',
        text = 'Penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin. Penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin. Penguin penguin penguin @penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin. Penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin penguin.')

    main.models.Tag.objects.create(name = 'Hashtag')
    main.models.Tag.objects.create(name = 'Chicken')
    main.models.Tag.objects.create(name = 'Bleep')
    main.models.Tag.objects.create(name = 'Bloop')
    
    comment1 = main.models.Comment.objects.create(
        username = 'sbrin',
        text = 'Great post @page. @tennien @tennien @tennien',
        post = post1)

    comment2 = main.models.Comment.objects.create(
        username = 'wacko',
        text = 'You make @killerrobots that will take over the world.',
        post = post1)

    comment3 = main.models.Comment.objects.create(
        username = 'security',
        text = 'Excuse me, @wacko, you\'re going to have to leave.',
        parent_comment = comment2)
    
    comment1.gen_reply_activity()
    comment1.gen_mention_activities()
    comment2.gen_reply_activity()
    comment2.gen_mention_activities()
    comment3.gen_reply_activity()
    comment3.gen_mention_activities()