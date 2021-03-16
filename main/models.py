from django.db import models
from account.models import User


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # update_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # class Meta:
    #     ordering = ['-posted_on']

    # def number_of_likes(self):
    #     if self.likes.count():
    #         return self.likes.count()
    #     else:
    #         return 0

    @property
    def likes(self):
        return self.like_set.filter(is_active=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    # video = models.FileField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('-created', )


class Like(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


class Favourite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=True)


class Rating(models.Model):
    RATE_CHOICES = (
        (4, "excellent"),
        (3, "very good"),
        (2, "good"),
        (1, "bad"),
    )

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES)


class History(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)