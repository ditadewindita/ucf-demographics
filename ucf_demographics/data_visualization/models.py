# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.db import models
from djongo import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class GenderData(models.Model):
    men = models.IntegerField()
    women = models.IntegerField()

    def __str__(self):
        return "Men: {0}, Women: {1}".format(str(self.men), str(self.women))

class EthnicityData(models.Model):
    ethnicity = models.CharField(max_length = 50)
    total = total = models.EmbeddedModelField(
        model_container=GenderData,
    )

    def __str__(self):
        return "Ethnicity: {0}, Total: {1}".format(str(self.ethnicity), str(self.total))

class DataByCollege(models.Model):
    college = models.CharField(max_length = 50)
    college_code = models.CharField(max_length = 50)
    data = models.ArrayModelField(
        model_container=EthnicityData,
    )
    total = models.EmbeddedModelField(
        model_container=GenderData,
    )
    university_total = models.IntegerField()
    term = models.CharField(max_length = 50)

    def __str__(self):
        return "College: {0}, Classification: {1}, Data: {2}, Total: {3}, University Total: {4}, Date: {5}".format(self.college, self.classification, self.data, self.total, str(self.university_total), self.date)
