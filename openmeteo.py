import requests
import json
import csv
import datetime
from numpy import sum, mean

now = datetime.datetime.now()

def get_statitics(start_date, end_date):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 34.9774,
        "longitude": 33.8489,
        "hourly": ["temperature_2m", "direct_radiation", "diffuse_radiation"],
        "start_date": start_date,
        "end_date": end_date
    }
    responses = requests.get(url, params=params)
    data = responses.json()
    temp_sum = round(sum(data["hourly"]["temperature_2m"])/24)
    temp_avg = round(mean(data["hourly"]["temperature_2m"]))
    sun_sum = round((sum(data["hourly"]["direct_radiation"]) + sum(data["hourly"]["diffuse_radiation"]))/24)
    sun_avg = round((mean(data["hourly"]["direct_radiation"]) + mean(data["hourly"]["diffuse_radiation"])))

    return temp_sum, temp_avg, sun_sum, sun_avg

def get_startdate(deviation):
   return (now - datetime.timedelta(days=deviation)).strftime("%Y-%m")

# Read which months we already have
with open("openmeteo.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    str_list = []

    for row in reader:
        str_list.append(f'{row[0]}-{row[1]}')

# Write new months
with open('openmeteo.csv', 'a', newline='') as csvfile:
    header = ['Year', 'Month', 'Temp Sum', 'Temp Avg', 'Sun Sum', 'Sun Avg']
    writer = csv.writer(csvfile, delimiter=';')

    for i in range (7, 0, -1):
        start_string = (get_startdate(i*30))
        if start_string not in str_list:
            temp_sum, temp_avg, sun_sum, sun_avg = get_statitics(f"{start_string}-01", f"{start_string}-30")
            writer.writerow([start_string[:4], start_string[5:8], temp_sum, temp_avg, sun_sum, sun_avg])
            print (f"{start_string} added")    

# Print the statistics of the current month
temp_sum, temp_avg, sun_sum, sun_avg = get_statitics(f"{now.year}-{now.month}-01", f"{now.year}-{now.month}-{now.day}")
print (f"Temp Sum: {temp_sum}")
print (f"Temp Avg: {temp_avg}")
print (f"Sun Sum: {sun_sum}")
print (f"Sun Avg: {sun_avg}")