import time
import datetime
import os
import pandas as pd

PATH = 'flight-data'

START_DATE = '05/08/2021'
END_DATE = '06/08/2021'

LOW_RANGE = 30
HIGH_RANGE = 1000

def date_to_unix(date):
    return time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())

folder = os.fsencode(PATH)
filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.csv') ):
        filenames.append(filename)

data = pd.DataFrame(columns=['snapshot_id', 'altitude', 'latitude', 'longitude'])

for filename in filenames[:20]:
    flight = pd.read_csv(f'{PATH}/{filename}')
    flight = flight[['snapshot_id', 'altitude', 'latitude', 'longitude']]
    data = pd.concat([data, flight])

# filter on height
data = data[(data.altitude > LOW_RANGE) & (data.altitude < HIGH_RANGE)]

# filter on date
unix_start = date_to_unix(START_DATE)
unix_end = date_to_unix(END_DATE)
data = data[(data.snapshot_id > unix_start) & (data.snapshot_id < unix_end)]

data.to_csv('filtered_points.csv')