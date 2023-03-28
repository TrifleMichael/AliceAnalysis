import json
from datetime import datetime


def log(information):
    f = open("LOGS", "a")
    f.write(str(datetime.now()))
    f.write(" : ")
    f.write(information)
    f.write("\n")
    f.close()
    print(information)

def parse_into_records(files):
    records = []
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:

                    record = {'timestamp': int(json_line['timestamp'])}

                    records.append(record)
    return records

def calculate_connections_start_dict(records):
    connections_start_dict = {}  # Key - timestamp, value - number of connections that start at that time
    for record in records:
        timestamp = record['timestamp']
        if timestamp not in connections_start_dict:
            connections_start_dict[timestamp] = 0
        connections_start_dict[timestamp] += 1
    return connections_start_dict

def fill_connection_start_dict_gaps(connections_start_dict):
    for timestamp in range(min(connections_start_dict), max(connections_start_dict)):
        if timestamp not in connections_start_dict:
            connections_start_dict[timestamp] = 0

def save_output(connections_start_dict, output_name):
    f = open(output_name(output_name), "w")
    for timestamp in connections_start_dict:
        f.write(str(timestamp) + ":" + str(connections_start_dict[timestamp]) + "\n")
    f.close()

def calculate_start_of_connections(input_names, output_name):
    log("Starting calculate_start_of_connections for " + output_name)
    records = parse_into_records(input_names)
    log("Records parsed")
    connections_start_dict = calculate_connections_start_dict(records)
    log("Start dictionary constructed")
    fill_connection_start_dict_gaps(connections_start_dict)
    log("Start dictionary gaps filled")
    save_output(connections_start_dict, output_name)
    log("Output saved")
