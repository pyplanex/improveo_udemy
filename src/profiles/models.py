from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid
import os
# Create your models here.


def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return os.path.join('uploads/profile/img', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to=get_upload_path, default='uploads/profile/img/avatar.png', validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    website = models.CharField(max_length=220)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.user)
