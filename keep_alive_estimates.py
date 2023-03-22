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

def timestamp_between(start, end, useragent, start_dict):
    lowest_inbounds = float('inf')
    for timestamp in start_dict[useragent]:
        if start < timestamp <= end:
            lowest_inbounds = min(lowest_inbounds, timestamp)
    return lowest_inbounds


def construct_start_dict(files):
    start_dict = {}  # Key - useragent, value - list of start timestamps for that useragent
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                # if i % 1000000 == 0:
                #     log("Parsing progress in double_checker: " + str(i))
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    useragent = json_line['useragent']
                    timestamp = int(json_line['timestamp'])

                    if useragent not in start_dict:
                        start_dict[useragent] = []
                    start_dict[useragent].append(timestamp)
    return start_dict

def construct_concurrent_dict(files, start_dict, keep_alive):
    parallelised = 0

    concurrent_dict = {}  # Key - timestamp, value - number of concurrent calls
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                # if i % 1000000 == 0:
                #     log("Parsing progress in double_checker: " + str(i))
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    useragent = json_line['useragent']
                    timestamp = int(json_line['timestamp'])
                    elapsed_ms = int(json_line['elapsed_ms'])
                    end_timestamp = timestamp + elapsed_ms

                    upper_bound = min(
                        end_timestamp + keep_alive,
                        timestamp_between(end_timestamp, end_timestamp + keep_alive, useragent, start_dict)
                    )

                    if upper_bound != end_timestamp+keep_alive:
                        parallelised += 1

                    for stamp in range(timestamp, upper_bound+1):
                        if stamp not in concurrent_dict:
                            concurrent_dict[stamp] = 0
                        concurrent_dict[stamp] += 1
    log("Parallel: "+str(parallelised))
    return concurrent_dict

def save_result(concurrent_dict, output_name):
    f = open(output_name, "w")
    for key in concurrent_dict:
        f.write(str(key) + ":" + str(concurrent_dict[key]) + "\n")
    f.close()

def keep_alive_estimates(file_paths, output_name, keep_alive):
    start_dict = construct_start_dict(file_paths)
    log("Start dict generated for " + str(file_paths))
    concurrent_dict = construct_concurrent_dict(file_paths, start_dict, keep_alive)
    log("Concurrent dict generated for " + str(file_paths))
    save_result(concurrent_dict, output_name)
    log("Results saved for " + str(file_paths))
