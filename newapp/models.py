from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


class UserProf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=30, null=True)
    user_type = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.user.username


class Login(models.Model):
    username = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.username


class LoginOperational(models.Model):
    username = models.CharField(max_length=150, null=True)
    fileop = models.FileField(upload_to="media", blank=False, null=False,
                              validators=[FileExtensionValidator(['pptx', 'docx', 'xlsx'])])

    def __str__(self):
        return self.username


class LoginClient(models.Model):
    username = models.CharField(max_length=150, null=True)
    username_file_uploader = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.username

