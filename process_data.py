# this whole thing is slower than what it could be
import csv 

selected_elabels = [ 
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'  
]

selected_elabels_set = set(selected_elabels)

selected_wlabels = [
    'temp',
    'temp_min',
    'temp_max',
    'pressure',
    'humidity',
    'wind_speed',
    'rain_1h',
    'rain_3h',
    'clouds_all'
]

selected_wlabels_set = set(selected_wlabels)

other_labels = ['year', 'month', 'day', 'time']

def parse_date(time_date):
    date, time = time_date.split(' ')
    year, month, day = date.split('-')
    time = time.split(':')[0]

    return (year, month, day, time)


def parse_labels(csv_file_reader):
    labels = None
    for row in csv_file_reader:
        labels = row
        break
    
    return labels


def process_row(raw_row, labels, selected_labels, dt_index  =1):
    row = list(zip(labels, raw_row))
    filtered = {key: float(value) for key, value in row if key in selected_labels}

    date_time =  parse_date(row[dt_index][1])

    return (date_time, filtered)


def process_weather():
    weatherf = open("clean_weather.csv", "r")
    weather_reader = csv.reader(weatherf, delimiter=',')

    labels = parse_labels(weather_reader)

    date_sum = {}
    for raw_row in weather_reader:
        date_time, filtered = process_row(raw_row, labels, selected_wlabels_set)

        # row[1] is dt_iso
        if  date_time in date_sum.keys():
            for key, val in filtered.items():
                date_sum[date_time][0][key] += val

            date_sum[date_time][1] += 1
        else:
            date_sum[date_time] = [filtered, 1]
        

    avg_weatherf = open("clean_weather_processed.csv", "w")
    avg_weather_writer = csv.writer(avg_weatherf, delimiter=',')
    avg_weather_writer.writerow(other_labels + list(selected_wlabels))

    for key, value in date_sum.items():
        year, month, day, time = key
        avgd_row = [year, month, day, time]

        for dict_key, dict_value in value[0].items():
            avgd_row.append(dict_value / value[1])
            

        avg_weather_writer.writerow(avgd_row)

    avg_weatherf.seek(0)
    avg_weatherf.close()
            
def process_energy():
    energyf = open('clean_energy.csv', 'r')
    energy_reader = csv.reader(energyf, delimiter=',')
    
    processed_energyf = open('clean_energy_processed.csv', 'w')
    proc_energy_writer = csv.writer(processed_energyf, delimiter=',')

    labels = parse_labels(energy_reader)
    
    proc_energy_writer.writerow(other_labels + list(selected_elabels))
    
    averages = {}
    entry_count = 0
    for raw_row in energy_reader:
        date_time, row = process_row(raw_row, labels, selected_elabels_set)
        for key, value in row.items():
            if key in averages:
                averages[key] += value
            else:
                averages[key] = value 
        entry_count+=1

    
    for key, val in averages.items():
        averages[key] = averages[key]/entry_count


    energyf.seek(0)
    
    for _ in energy_reader:
        break

    for raw_row in energy_reader:
        date_time, row = process_row(raw_row, labels, selected_elabels_set)
        year, month, day, time = date_time
        
        proc_row = [year, month, day, time]
        proc_row = proc_row + [val/averages[key] for key, val in row.items()]

        proc_energy_writer.writerow(proc_row)

    processed_energyf.seek(0)
    processed_energyf.close()



def compare_times(time1, time2):
    time1 = [int(i) for i in time1]
    time2 = [int(i) for i in time2]
    
    retval = time1[0] == time2[0] and time1[1] == time2[1]
    retval = retval and time1[2] == time2[2] and time1[3] == time2[3]

    return retval


def main():
    process_energy()
    process_weather()
    energyf = open('clean_energy_processed.csv', 'r')
    weatherf = open('clean_weather_processed.csv', 'r')
    weather_energyf = open('clean_weather_energy.csv', 'w')
   

    energy_reader = csv.reader(energyf, delimiter=',')
    weather_reader = csv.reader(weatherf, delimiter=',')
    weather_energy_writer = csv.writer(weather_energyf, delimiter=',')


    weather_energy_writer.writerow(other_labels + selected_wlabels + selected_elabels)

    count = 0
    for raw_erow in energy_reader:
        if raw_erow[0] == 'year':
            continue

        for raw_wrow in weather_reader:
            if raw_wrow[0] == 'year':
                continue
            
            if compare_times(raw_erow[:4], raw_wrow[:4]):
                proc_row = raw_wrow + raw_erow[4:]
                print(str(count), end = '\r')
                count += 1
                weather_energy_writer.writerow(proc_row)
                break

        weatherf.seek(0)
main()