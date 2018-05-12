# UCF Demographics
With over 60,000 students, UCF has a mixture of people from vastly different backgrounds. This Django project aims to visualize UCF's diversity by aggregating data from the official [UCF Fact Book](https://ikm.ucf.edu/facts-and-reports/ucf-fact-book/) and plotting it to conceptualize diversity over the course of the years in specific colleges and the overall student population.

Created By: Haerunnisa Dewindita

## To Run
Once initial release is ready, web app will be deployed with `Heroku`. Meanwhile,
you can clone the project and run it locally:

```
$ git clone https://github.com/ditadewindita/ucf-demographics.git
$ python3 manage.py runserver
```

`pip install` any required dependencies.

## Technologies
- Python 3.6
- Django 2.0
- Djongo/PyMongo (MongoDB wrapper for Django)
- Bokeh 12.15

## To-Do
- ~~Setup DB~~
- ~~Setup Django env~~
- ~~Connect backend~~
- ~~Create initial Bokeh graph for total university~~
  - ~~With stacked `HBars` and `HoverTools`~~
  - Create more detailed hover tools
- Create initial layout with Bootstrap
- Collect data & turn to CSV:
  - ~~Fall 2016~~
  - Spring 2017
  - Summer 2017
  - Fall 2017
  - Spring 2018
- ~~Create python script to parse CSV to JSON and register to DB~~
- Deploy to Heroku
