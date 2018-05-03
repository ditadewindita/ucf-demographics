# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djongo import models

# Create your models here.
class GenderData(models.Model):
    men = models.IntegerField()
    women = models.IntegerField()

    def __str__(self):
        return self.name

class EthnicityData(models.Model):
    ethnicity = models.CharField(max_length = 50)
    men = models.IntegerField()
    women = models.IntegerField()

    def __str__(self):
        return self.name

class DataByCollege(models.Model):
    college = models.CharField(max_length = 50)
    classification = models.CharField(max_length = 50)
    data = models.ArrayModelField(
        model_container=EthnicityData,
    )
    total = models.EmbeddedModelField(
        model_container=GenderData,
    )
    university_total = models.IntegerField()
    date = models.CharField(max_length = 50)
