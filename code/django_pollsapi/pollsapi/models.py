from __future__ import unicode_literals

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(max_length=100)
    created_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices')
    choice_text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='votes')
    poll = models.ForeignKey(Poll)
    voted_by = models.ForeignKey(User)

    class Meta:
        unique_together = ("poll", "voted_by")
