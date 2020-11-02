import pandas as pd
from datetime import datetime, time

from os.path import dirname, join

from bokeh.layouts import column
from bokeh.models import Select, ColumnDataSource
from bokeh.plotting import figure, curdoc, show

# Go through chunks of csv cuz file is huge
row_count = 1000


# Compute hours from created to closed time in hours
def get_hour_difference(timestamp1, timestamp2):
    date1 = datetime.strptime(timestamp1, '%m/%d/%Y %H:%M:%S %p')
    date2 = datetime.strptime(timestamp2, '%m/%d/%Y %H:%M:%S %p')
    date_diff = date2-date1
    return date_diff.total_seconds()/3600

# return an int indicating the month of the date
def get_month(timestamp):
    date = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S %p')
    return date.month


month_num =[1,2,3,4,5,6,7,8,9,10,11,12]

# Set to store all zip codes
list_of_zips = set()
# Dicts to store cases and resolution times
cases_by_zip = dict()
all_cases = dict()
# Add months to dict
for month in month_num:
    all_cases[month] = list()
    cases_by_zip[month] = list()


# Keep three columns: Start date, Resolved date and zip
df = pd.read_csv('filtered_cols_2020.csv', delimiter=",")
#for chunk in pd.read_csv(join(dirname(__file__), 'data', 'filtered_cols_2020.csv'), chunksize=row_count, delimiter=",", encoding="utf-8"):#, usecols=[1,2,8]):
# column with all zip codes of chunk
zip_code_col = df.iloc[:,-1].to_numpy()
# column with all creating time information
date_created_col = df.iloc[:,0].to_numpy()
# column with all closed dates
date_closed_col = df.iloc[:,1].to_numpy()

#tuple_info = list(zip(zip_code_col,date_created_col, date_closed_col))

for zip_code, created, closed in zip(zip_code_col, date_created_col, date_closed_col):
    # Get month associated with entry
    zip_code = str(int(zip_code))
    month = get_month(closed)
    resolution_time = get_hour_difference(created, closed)
    # Add to all cases dict
    if resolution_time > 0:
        all_cases[month].append(get_hour_difference(created, closed))
# Store zip codes in dict
        if zip_code not in cases_by_zip:
            # Initialize zip code to track info for all months
            cases_by_zip[zip_code] = dict()
            list_of_zips.add(zip_code)
            # Initialize months to store information by month
            for this_month in month_num:
                cases_by_zip[zip_code][this_month] = list()
            # Add hour difference to zip_code list
            cases_by_zip[zip_code][month].append(resolution_time)
        else:
            cases_by_zip[zip_code][month].append(resolution_time)
    

# Dict to store monthly averages by zip
for zip_code in cases_by_zip.keys(): 
    for month in cases_by_zip[zip_code]:
        count = 0
        num_elems = 0
        for element in cases_by_zip[zip_code][month]:
            count += element
            num_elems += 1
        if num_elems > 0:
            count /= num_elems
        cases_by_zip[zip_code][month] = count

# Dict to store overall monthly averages
monthly_averages = dict()
for month in month_num:
    num_elems = len(all_cases[month])
    if num_elems > 0:
        monthly_averages[month] = sum(all_cases[month])/num_elems
    else:
        monthly_averages[month] = 0

# Convert zip codes into types to be used in Dropdown
zip_tuples = list()
 
for zipo in list_of_zips:
    to_s = str(int(zipo))
    zip_tuples.append((to_s, to_s))

#zip_tuples.sort()

import csv

# Write csv that contains monthly averages by zip 
with open('data.csv', 'w') as f:
        for zip_code in cases_by_zip.keys():
            for month in cases_by_zip[zip_code]:
                f.write("%s, %s, %s\n" % (zip_code, month, cases_by_zip[zip_code][month]))

with open('overall.csv', 'w') as f:
        for month in month_num:
            f.write("%s, %s\n" % (month, monthly_averages[month]))
