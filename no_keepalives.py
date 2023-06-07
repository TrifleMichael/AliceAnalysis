import json
from datetime import datetime
from collections import deque

# Tworzy plik z danymi o wykresie polaczen po czasie

def log(information):
    f = open("LOGS", "a")
    f.write(str(datetime.now()))
    f.write(" : ")
    f.write(information)
    f.write("\n")
    f.close()
    print(information)

def parse_into_records(files):
    records = deque([])
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                if i % 1000000 == 0:
                    print(i // 1000000, "mln")
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    record = (int(json_line['timestamp']),
                              int(json_line['elapsed_ms']))
                    records.append(record)
    return records


def sort_records(records):
    return sorted(records, key=lambda record: record[0])


def construct_concurrent_dict(records):
    concurrent_dict = {}  # Key - timestamp, value - number of concurrent calls

    i = 0
    while len(records) != 0:
        i += 1
        if i % 1000000 == 0:
            print(i // 1000000, "mln")

        record = records.pop()
        timestamp = record[0]
        end_timestamp = record[0] + record[1]

        for stamp in range(timestamp, end_timestamp):
            if stamp not in concurrent_dict:
                concurrent_dict[stamp] = 0
            concurrent_dict[stamp] += 1
    return concurrent_dict


def fill_dict_gaps(dict):
    for i in range(min(dict), max(dict)):
        if i not in dict:
            dict[i] = 0


def save_result(concurrent_dict, output_name):
    f = open(output_name, "w")
    for timestamp in range(min(concurrent_dict), max(concurrent_dict)+1):
        f.write(str(timestamp) + ":" + str(concurrent_dict[timestamp]) + "\n")
    f.close()


def no_keepalive(file_paths, output_name):
    log("Analysis without keep alives starting for " + output_name)
    records = parse_into_records(file_paths)
    log("Records parsed")
    records = sort_records(records)
    log("Records sorted")
    concurrent_dict = construct_concurrent_dict(records)
    log("Concurrent dict generated for " + str(file_paths))
    fill_dict_gaps(concurrent_dict)
    log("Filled concurrent dict gaps")
    save_result(concurrent_dict, output_name)
    log("Results saved for " + output_name)
