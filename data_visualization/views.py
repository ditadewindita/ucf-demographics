# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
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

def get_chart(college_code, term, year):
        try:
            by_college_data = DataByCollege.objects.get(college_code = college_code, term = term, year = year)
        except:
            return (None, None)

        college = by_college_data.college
        title = "%s in %s %s" % (college, by_college_data.term, str(year))
        ethnicities = [c.ethnicity for c in by_college_data.data]
        ethnicity_ratio = [(e.total.men + e.total.women) * 100 / by_college_data.university_total for e in by_college_data.data]
        genders = ["Men", "Women"]
        colors = ["#C9A61A", "#E0C970"]
        men = [c.total.men for c in by_college_data.data]
        women = [c.total.women for c in by_college_data.data]

        data = { 'ethnicities' : ethnicities,
            'EthnicityRatio' : ethnicity_ratio,
            'Men' : men,
            'Women' : women,
            'MenRatio' : [men[i] * 100 / (men[i] + women[i]) if (men[i] + women[i]) != 0 else 0 for i in range(len(men))],
            'WomenRatio' : [women[i] * 100 / (men[i] + women[i]) if (men[i] + women[i]) != 0 else 0 for i in range(len(women))],
            'EthnicityTotal' : [e.total.men + e.total.women for e in by_college_data.data]
        }

        # Whole bar stats
        # hover = HoverTool(tooltips = [
        #     ("Men", "@Men (@MenRatio{0.2f}%)"),
        #     ("Women", "@Women (@WomenRatio{0.2f}%)")
        # ])

        hover = HoverTool(tooltips = """
            <div class="container-fluid" style="margin:5px;">
                <div class="row justify-content-center">
                    <h4>@ethnicities</h4>
                </div>

                <div class="row justify-content-center" style="font-size:14px;">
                    <div class="col text-center">
                        <span style="font-weight: bold;">@MenRatio{0.2f}%</span>
                        <br>Men (@Men)
                    </div>
                    <div class="col text-center">
                        <span style="font-weight: bold;">@WomenRatio{0.2f}%</span>
                        <br>Women (@Women)
                    </div>
                </div>

                <div class="row justify-content-center" style="margin-top:5px;">
                    <span>@ethnicities students (@EthnicityTotal) make up&nbsp;</span>
                    <span style="font-weight: bold;">@EthnicityRatio{0.2f}%</span>
                    <span>&nbsp;of the """ + title + """.</span>
                </div>
            </div>
        """)

        # ticker = SingleIntervalTicker(interval = 1000, num_minor_ticks = 0)
        # xaxis = LinearAxis(ticker = ticker, axis_label = 'Number of Students')

        plot = figure(y_range = ethnicities, plot_height = 200, sizing_mode = 'scale_width', title = title, toolbar_location = None, tools = [hover])
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

def college_data(college_code, year):
    terms = ["Spring", "Summer", "Fall"]
    # script, div, college, college_code = get_chart(college_code, term, year)
    term_data = []
    college = DataByCollege.objects.filter(college_code = college_code).first().college

    context = {
        'term_data' : term_data,
        'college_code' : college_code,
        'college' : college
    }

    for term in terms:
        script, div = get_chart(college_code, term, year)

        if script != None and div != None:
            term_context = {
                'script' : script,
                'div': div
            }
            term_data.append(term_context)

    return context

def all_college_data_by_year(year):
    data = []
    colleges = ["ALL", "CAH", "CBA", "CEDHP", "CECS", "GA", "COHPA", "COM", "CON", "CREOL", "COS", "UGST", "RCHM", "UNDC"]
    years = DataByCollege.objects.values('year').distinct().order_by('year')

    for college_code in colleges:
        curr_context = college_data(college_code, year)
        data.append(curr_context)

    context = {
        'data' : data,
        'years' : years
    }

    return context

def year(request, year):
    context = all_college_data_by_year(year)

    return render(request, 'data_visualization/year.html', context)

def index(request):
    years = DataByCollege.objects.values('year').distinct().order_by('-year')
    year = years.first()['year']
    context = all_college_data_by_year(year)

    return render(request, 'data_visualization/index.html', context)
