from django.db import models


class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20, default="")
    first_login = models.BooleanField(default=False)


class SavedNews(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=300, default="")
    news_title = models.CharField(max_length=500, default="")
    news_description = models.TextField(max_length=1000, default="")
    news_source = models.CharField(max_length=200, default="")
