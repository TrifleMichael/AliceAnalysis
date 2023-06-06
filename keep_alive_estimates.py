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
                if i % 1000000 == 0:
                    print(i // 1000000, "mln")
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:

                    record = (json_line['userAgent'],
                              int(json_line['timestamp']),
                              int(json_line['elapsed_ms']))

                    records.append(record)
    return records

def sort_records(records):
    return sorted(records, key=lambda record: record[1])

# Returns last end timestamp from that user that happened before timestamp.
def get_last_end(useragent, timestamp, end_dict):
    for i in range(len(end_dict[useragent])-1, -1, -1):
        if end_dict[useragent][i] < timestamp:
            return end_dict[useragent].pop(i)
    return None

# Returns dictionary that holds information about which records can be merged
def construct_end_nextstart_dict(records):
    end_nextstart_dict = {}  # key - user, value - dictionary of (key - end timestamp, value - next start)
    end_dict = {}  # key - user, value - list of ends of their connections (sorted by start time of those connections) # TODO: This algorithm will be inaccurate if a user can have two connections at the same time. Check that.
    for record in records:

        # Add record data to end_dict
        useragent = record[0]
        timestamp = record[1]
        elapsed_ms = record[2]
        end_timestamp = timestamp + elapsed_ms
        if useragent not in end_dict:
            end_dict[useragent] = []
        end_dict[useragent].append(end_timestamp)

        # Try to find last end
        last_end = get_last_end(useragent, timestamp, end_dict)
        if last_end is not None:
            if useragent not in end_nextstart_dict:
                end_nextstart_dict[useragent] = {}
            end_nextstart_dict[useragent][last_end] = timestamp

    return end_nextstart_dict

def construct_concurrent_dict(records, end_nextstart_dict, keep_alive):
    concurrent_dict = {}  # Key - timestamp, value - number of concurrent calls

    while len(records) != 0:
        record = records.pop()
    # for record in records:
        useragent = record[0]
        timestamp = record[1]
        elapsed_ms = record[2]
        end_timestamp = timestamp + elapsed_ms

        if (useragent in end_nextstart_dict) and (end_timestamp in end_nextstart_dict[useragent]):
            next_start = end_nextstart_dict[useragent][end_timestamp]
        else:
            next_start = float('inf')

        # Next start can be within the keepalive window or beyond that window.
        upper_bound = min(
            end_timestamp + keep_alive,
            next_start
        )

        for stamp in range(timestamp, upper_bound+1):
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
    for timestamp in range(min(concurrent_dict), max(concurrent_dict)):
        f.write(str(timestamp) + ":" + str(concurrent_dict[timestamp]) + "\n")
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
    fill_dict_gaps(concurrent_dict)
    log("Filled concurrent dict gaps")
    save_result(concurrent_dict, output_name)
    log("Results saved for " + output_name)
