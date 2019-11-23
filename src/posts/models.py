from django.db import models
from profiles.models import Profile
from reports.models import Report, ProblemReported
from django.core.validators import FileExtensionValidator
from django.urls import reverse
import uuid
import os
# Create your models here.

LIKE_CHOICES = (
    ("Like", "Like"),
    ("Unlike", "Unlike"),
)


class PostManager(models.Manager):
    def public_only(self):
        return self.filter(problem_reported__public=True)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked = models.ManyToManyField(Profile, related_name="liked", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def num_likes(self):
        return self.liked.all().count()


class ProblemPost(Post):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    problem_reported = models.ForeignKey(
        ProblemReported, on_delete=models.CASCADE)

    objects = PostManager()

    def __str__(self):
        return "{}".format(self.problem_reported.description[:50])

    def get_absolute_url(self):
        return reverse("posts:pp-detail", kwargs={"pk1": self.pk, 'pk': self.problem_reported.id})


def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return os.path.join('uploads/posts/img', filename)


'''
1. specify the path static_cdn -> media_root -> uploads -> images
2. picture1.png -> 59afab01-6482-4f18-9527-f60e18def5fa.png
'''


class GeneralPost(Post):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=360)
    image = models.ImageField(upload_to=get_upload_path, blank=True, validators=[
                              FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("posts:gp-detail", kwargs={"pk": self.pk})


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default="Like", max_length=10)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        GeneralPost, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=360)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.pk)

    class Meta:
        ordering = ('-created',)
