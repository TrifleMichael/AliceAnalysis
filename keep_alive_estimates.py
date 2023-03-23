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

                    record = {'useragent': json_line['userAgent'],
                              'timestamp': int(json_line['timestamp']),
                              'elapsed': int(json_line['elapsed_ms'])}

                    records.append(record)
    return records

def sort_records(records):
    return sorted(records, key=lambda record: record['timestamp'])

# Returns last end timestamp from that user that happened before timestamp.
def get_last_end(useragent, timestamp, end_dict):
    for i in range(len(end_dict[useragent])-1, -1, -1):
        if end_dict[useragent][i] < timestamp:
            return end_dict[useragent].pop(i)
    return None


def construct_end_nextstart_dict(records):
    end_nextstart_dict = {}  # key - user, value - dictionary of (key - end timestamp, value - next start)
    end_dict = {}  # key - user, value - list of ends of their connections (sorted by start time of those connections)
    for record in records:

        # Add record data to end_dict
        useragent = record['useragent']
        timestamp = record['timestamp']
        end_timestamp = record['timestamp'] + record['elapsed_ms']
        if useragent not in end_dict:
            end_dict[useragent] = []
        end_dict[useragent].append(end_timestamp)

        # Try to find last end
        last_end = get_last_end(useragent, timestamp, end_dict)
        if last_end is not None:
            end_nextstart_dict[useragent][last_end] = timestamp

    return end_nextstart_dict

# def construct_concurrent_dict(files, start_dict, keep_alive):
def construct_concurrent_dict(records, end_nextstart_dict, keep_alive):
    concurrent_dict = {}  # Key - timestamp, value - number of concurrent calls

    for record in records:
        timestamp = record['timestamp']
        useragent = record['useragent']
        end_timestamp = record['timestamp'] + record['elapsed_ms']

        if end_timestamp in end_nextstart_dict[useragent]:
            next_start = end_nextstart_dict[useragent][end_timestamp]
        else:
            next_start = float('inf')

        upper_bound = min(
            end_timestamp + keep_alive,
            next_start
        )

        for stamp in range(timestamp, upper_bound+1):
            if stamp not in concurrent_dict:
                concurrent_dict[stamp] = 0
            concurrent_dict[stamp] += 1
    return concurrent_dict

def save_result(concurrent_dict, output_name):
    f = open(output_name, "w")
    for key in concurrent_dict:
        f.write(str(key) + ":" + str(concurrent_dict[key]) + "\n")
    f.close()

def keep_alive_estimates(file_paths, output_name, keep_alive):
    records = parse_into_records(file_paths)
    log("Records parsed")
    records = sort_records(records)
    log("Records sorted")
    end_nextstart_dict = construct_end_nextstart_dict(records)
    log("End-nextstart dict constructed")
    concurrent_dict = construct_concurrent_dict(records, end_nextstart_dict, keep_alive)
    log("Concurrent dict generated for " + str(file_paths))
    save_result(concurrent_dict, output_name)
    log("Results saved for " + str(file_paths))
