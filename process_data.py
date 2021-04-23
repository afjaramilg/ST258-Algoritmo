import csv 

elabels = None
wlabels = None

max_col_elabels = {}
max_col_wlabels = {}


selected_elabels = [ 
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'  
]

selected_wlabels = [
    'temp',
    'temp_min',
    'temp_max',
    'pressure',
    'humidity',
    'wind_speed',
    'rain_1h',
    'rain_3h',
    'clouds_all',
    'weather_id',
]


other_labels = ['time']

def parse_date(time_date):
    date, time = time_date.split(' ')
    _, month, day = date.split('-')
    time = time.split(':')[0]

    return (month, day, time)

def combine_rows(energy_row, weather_row):
    
    month, day, time = parse_date(weather_row[wlabels['dt_iso']])
    combined = [time]


    for l in selected_wlabels:
        combined.append(weather_row[wlabels[l]])

    for l in selected_elabels:
        combined.append(energy_row[elabels[l]])

    return combined


def parse_labels(csv_file_reader):
    raw_labels = None
    labels = {}
    for row in csv_file_reader:
        raw_labels = row
        break

    index = 0
    for label in raw_labels:
        labels[label] = index
        index+=1
    
    return labels


def main():
    weatherf = open("clean_weather.csv", "r")
    energyf = open("clean_energy.csv", "r")
    combinedf = open("clean_weather_energy.csv", "w")

    energy_reader = csv.reader(energyf, delimiter=',')
    weather_reader = csv.reader(weatherf, delimiter=',')
    combined_writer = csv.writer(combinedf, delimiter=',')

    global elabels
    global wlabels
    
    elabels = parse_labels(energy_reader)
    wlabels = parse_labels(weather_reader)

    combined_writer.writerow(other_labels + selected_wlabels  + selected_elabels)

    #combined_writer.writerow(selected_wlabels  + selected_elabels)
    for energy_row in energy_reader:
        for l in selected_elabels:
            if l in max_col_elabels:
                max_col_elabels[l] = max(max_col_elabels[l], elabels[l])
            else:
                max_col_elabels[l] = 0 


    for weather_row in weather_reader:
        for l in selected_wlabels:
            if l in max_col_wlabels:
                max_col_wlabels[l] = max(max_col_wlabels[l], wlabels[l])
            else:
                max_col_wlabels[l] = 0 


    energyf.seek(0)
    weatherf.seek(0)

    for energy_row in energy_reader:
        for weather_row in weather_reader:
            if energy_row[1] == weather_row[1]:
                combined_row = combine_rows(energy_row, weather_row)
                combined_writer.writerow(combined_row)
                break

main()

