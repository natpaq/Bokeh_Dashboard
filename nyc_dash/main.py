import csv
import pandas as pd

from bokeh.layouts import column
from bokeh.models import Select, ColumnDataSource
from bokeh.plotting import figure, curdoc, show
from datetime import datetime, time
from os.path import dirname, join


# Functions to modify plots based on zip code selection

def change_zip1(attr, old, new):
    # Store zip code that we're currently dealing with
    zip_code = int(dropdown.value)
    data1.data = {'x_values': month_num, "y_values": list(my_dict[zip_code].values())}

def change_zip2(attr, old, new):
    zip_code = int(dropdown2.value)
    data2.data = {'x_values': month_num, "y_values": list(my_dict[zip_code].values())}
    

month_num =[1,2,3,4,5,6,7,8,9,10,11,12]


# Extract Zip-Month-Average information from csv
df = pd.read_csv(join(dirname(__file__), 'data', 'data.csv'), delimiter=",", header=None)

# column with averages
average_col = df.iloc[:,-1].to_numpy()
# column with zip code information
zip_code_col = df.iloc[:,0].to_numpy()
# column with all months
month_col = df.iloc[:,1].to_numpy()

tupled = list(zip(zip_code_col, month_col, average_col))

# Prepare dict to store monthly average by zip
zips = set()
my_dict = dict()
for zipc, month, av in tupled:
    zips.add(zipc)
    if zipc not in my_dict:
        my_dict[zipc] = dict()
        my_dict[zipc][month] = av
    else:
        my_dict[zipc][month] = av

# Prepare stuff to plot overall averages
die = pd.read_csv(join(dirname(__file__), 'data', 'overall.csv'), delimiter=",", header=None)
month_col = die.iloc[:,0].to_numpy()
overall_av_col = die.iloc[:,1].to_numpy()

overall_av = dict()
for month, average in zip(month_col, overall_av_col):
    overall_av[month] = average

# Convert zip codes into types to be used in Dropdown
zip_tuples = list()
for zipo in zips:
    to_s = str(int(zipo))
    zip_tuples.append((to_s, to_s))

# Sort zip codes
zip_tuples.sort()

data1 = ColumnDataSource(data={'x_values': month_num, "y_values": list(my_dict[10000].values())})
data2 = ColumnDataSource(data={'x_values': month_num, "y_values": list(my_dict[10000].values())})

plot = figure(plot_width=600, plot_height=600, x_axis_label='Months', y_axis_label='Average Created-Closed Time (hours)')
dropdown = Select(title="Zipcode 1", value="10000", options=zip_tuples)
# Plot line for zip code 1
previous_zip1 = plot.line(x='x_values', y="y_values", line_width=2, line_color="red", name="line1", legend_label='zip code 1', source=data1)
dropdown.on_change("value", change_zip1)
dropdown2 = Select(title="Zipcode 2", value="10000", options=zip_tuples)
previous_zip2 = plot.line(x="x_values", y="y_values", line_width=2, line_color="green", name="line2", legend_label='zip code 2', source=data2)
dropdown2.on_change("value", change_zip2)


# for plot of all incidences in 2020
plot.line(month_num, list(overall_av.values()), line_width=2, legend_label='all')

curdoc().add_root(column(dropdown, dropdown2, plot))

