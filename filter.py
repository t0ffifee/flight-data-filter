import time
import datetime
import os
import pandas as pd

PATH = 'flight-data'

LOW_RANGE = 30
HIGH_RANGE = 1000

START_DATE = '05/08/2021'
END_DATE = '06/08/2021'

START_HOUR = 9
END_HOUR = 17

def date_to_unix(ts):
    return time.mktime(datetime.datetime.strptime(ts, "%d/%m/%Y").timetuple())

def good_time(row):
    flight = datetime.datetime.fromtimestamp(row['snapshot_id'])
    start = flight.replace(hour=START_HOUR, minute=0)
    end = flight.replace(hour=END_HOUR, minute=0)
    return start < flight and flight < end

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

# filter on time
data = data[data.apply(good_time, axis=1)]

data.to_csv('filtered_points.csv')