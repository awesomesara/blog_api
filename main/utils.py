from datetime import datetime
from main.models import History


def add_post(instance, user):
    if user.is_authenticated:
        post = History.objects.get_or_create(user=user, post=instance)[0]
        created_at = datetime.now()
        user.created_at = created_at
        user.post = post
        user.save()
    return user




















