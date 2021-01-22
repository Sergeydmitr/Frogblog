from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.aggregates import Count
from random import randint


class Article(models.Model):
    title = models.CharField(max_length = 100)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})


class RandomFactsManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Fact(models.Model):
    objects = RandomFactsManager()
    fact = models.TextField()

    def __str__(self):
        return self.fact


class Comment(models.Model):
    text = models.CharField(max_length = 200)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    approved = models.BooleanField(default=True)


    class Meta:
        ordering = ['-date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author)
