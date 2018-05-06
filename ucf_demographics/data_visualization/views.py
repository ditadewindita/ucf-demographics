# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from math import pi

# plots
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import SingleIntervalTicker, LinearAxis

# models
from .models import DataByCollege, EthnicityData, GenderData

def get_chart(college, term):
        try:
            by_college_data = DataByCollege.objects.get(college = college, term = term)
        except DataByCollege.DoesNotExist:
            raise HttpResponse(status = 404)

        title = "%s in %s" % (by_college_data.college, by_college_data.term)
        ethnicities = [c.ethnicity for c in by_college_data.data]
        genders = ["Men", "Women"]
        colors = ["#C9A61A", "#E0C970"]
        men = [c.total.men for c in by_college_data.data]
        women = [c.total.women for c in by_college_data.data]

        data = { 'ethnicities' : ethnicities,
            'Men' : men,
            'Women' : women,
            'MenRatio' : [men[i] * 100 / (men[i] + women[i]) for i in range(len(men))],
            'WomenRatio' : [women[i] * 100 / (men[i] + women[i]) for i in range(len(women))]
        }

        # Whole bar stats
        hover = HoverTool(tooltips = [
            ("Men", "@Men (@MenRatio{0.2f}%)"),
            ("Women", "@Women (@WomenRatio{0.2f}%)")
        ])

        # ticker = SingleIntervalTicker(interval = 1000, num_minor_ticks = 0)
        # xaxis = LinearAxis(ticker = ticker, axis_label = 'Number of Students')

        plot = figure(y_range = ethnicities, plot_height = 300, plot_width = 1000, title = title, toolbar_location = None, tools = [hover])
        renderers = plot.hbar_stack(genders, y = 'ethnicities', height = 0.4, color = colors, source = ColumnDataSource(data), legend = [value(g) for g in genders], name = genders)

        # plot.add_layout(xaxis, 'below')

        # # Stack bar specific tooltip
        # for r in renderers:
        #     gender = r.name
        #     if gender == 'Men':
        #         hover = HoverTool(tooltips=[
        #             ("Men", "@Men (@MenRatio{0.2f}%)")
        #             ], renderers = [r])
        #     else:
        #         hover = HoverTool(tooltips=[
        #             ("Women", "@Women (@WomenRatio{0.2f}%)")
        #             ], renderers = [r])
        #     plot.add_tools(hover)

        # plot.y_range.range_padding = 0.05
        # plot.x_range.start = 0
        plot.ygrid.grid_line_color = None
        plot.legend.location = "bottom_right"
        plot.axis.minor_tick_line_color = None
        plot.outline_line_color = None
        plot.xaxis.major_label_orientation = pi/4

        script, div = components(plot)
        return (script, div)

def college_data(request, college, term):
    if request.method == 'GET':
        script, div = get_chart(college, term)
        context = {
            'script' : script,
            'div': div
        }

        return HttpResponse(script, div)

def index(request):
    # college = "Total"
    # term = "Fall 2016"
    # script, div = get_chart(college, term)
    context = {
        # 'script' : script,
        # 'div': div
    }

    return render(request, 'data_visualization/index.html', context)
