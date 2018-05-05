# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import GenderData, EthnicityData, DataByCollege

admin.site.register(GenderData)
admin.site.register(EthnicityData)
admin.site.register(DataByCollege)
