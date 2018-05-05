# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# models
from .models import DataByCollege, EthnicityData, GenderData

def index(request):
    try:
        by_college_data = DataByCollege.objects.get(college = "Total").limit(1)
    except DataByCollege['DoesNotExist']:
        raise HttpResponse(status = 404)

    context = {
        'by_college_data': by_college_data,
    }
    return render(request, 'data_visualization/index.html', context)
