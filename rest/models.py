from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Island(models.Model):
    name = models.CharField(max_length=30)
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.TextField()
    owner = models.ForeignKey(User)
    rank = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.name

class Message(models.Model):
    text = models.TextField()
    topic = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    dest = models.ForeignKey('Island')
    
    def __unicode__(self):
        return self.text[:20]
