# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# plots
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from pandas import DataFrame as pd

# models
from .models import DataByCollege, EthnicityData, GenderData

def index(request):
    try:
        by_college_data = DataByCollege.objects.get(college = "Total")
    except DataByCollege.DoesNotExist:
        raise HttpResponse(status = 404)

    title = "University Total in %s" % (by_college_data.date)
    ethnicities = [c.ethnicity for c in by_college_data.data]
    genders = ["Men", "Women"]
    colors = ["#56C1F0", "#FF8686"]
    men = [c.total.men for c in by_college_data.data]
    women = [c.total.women for c in by_college_data.data]

    data = { 'ethnicities' : ethnicities,
        'Men' : men,
        'Women' : women,
        'MenRatio' : [men[i] * 100 / (men[i] + women[i]) for i in range(len(men))],
        'WomenRatio' : [women[i] * 100 / (men[i] + women[i]) for i in range(len(women))]
    }

    hover = HoverTool(tooltips = [
        ("Men", "@Men (@MenRatio{0.2f}%)"),
        ("Women", "@Women (@WomenRatio{0.2f}%)")
    ])

    plot = figure(y_range = ethnicities, plot_height = 400, title = title, toolbar_location = None, tools = [hover])
    plot.hbar_stack(genders, y = 'ethnicities', height = 0.4, color = colors, source = ColumnDataSource(data), legend = [value(g) for g in genders])

    # plot.y_range.range_padding = 0.05
    # plot.x_range.start = 0
    plot.ygrid.grid_line_color = None
    plot.legend.location = "bottom_right"
    plot.axis.minor_tick_line_color = None
    plot.outline_line_color = None

    script, div = components(plot)
    context = {
        'by_college_data': by_college_data,
        'script' : script,
        'div': div
    }

    return render(request, 'data_visualization/index.html', context)
