from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Form(models.Model):
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    text = models.TextField()
    email_subject = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)


class FormFields(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form')
    field_title = models.CharField(max_length=255)
    teg = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    must = models.BooleanField(default=False)


class Application(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='application')
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # fathers_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    # address = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user', null=True)
    text = models.TextField()
    key = models.CharField(max_length=4)
    signature = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
    link = models.CharField(max_length=255, blank=True)


class ApplicationFields(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="application_field")
    field_title = models.CharField(max_length=255)
    input = models.CharField(max_length=255)






