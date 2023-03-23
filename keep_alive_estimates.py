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

# def binary_search(list, searched_value):
#     if searched_value < list[0] or list[-1] < searched_value:
#         return None  # Should not happen
#     ind = len(list) // 2
#     l = 0
#     r = len(list) - 1
#     while l != r:
#         if list[ind] < searched_value:
#             l = ind
#         elif searched_value < list[ind]:
#             r = ind
#         elif searched_value == list[ind]:
#             return ind
#         # elif ind+1 < len(list) and list[ind] < searched_value < list[ind+1]:
#         #     return ind
#         ind = (r - l) // 2
#     return ind

# Returns the next timestamp after start, that belongs to useragent
# def next_useragent_timestamp(start, useragent, start_dict):
#
#     # Find the start index
#     ind = binary_search(start_dict[useragent], start)
#     if ind is None:
#         log("Terrible error in timestamp_between")
#
#     if ind+1 < len(start_dict[useragent]):
#         # If next value exists then return it
#         return start_dict[useragent][ind+1]
#     else:
#         return float('inf')

# TODO: Check if entries are chronological. If so, then next_useragent_timestamp can avoid sorting
#       by using a map of [useragent*timestamp]-[next_timestamp] for finding the next timestamp.
#       The map can be created in construct_start_dict.
#  ^ THEY SEEM TO BE
def construct_last_call_dict(files):
    last_from_user = {}  # Key - useragent, value - their last timestamp
    last_call_dict = {}  # Key - useragent, value - dictionary with (key - timestamps, value - next timestamp from that user)
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    useragent = json_line['userAgent']
                    timestamp = int(json_line['timestamp'])

                    if useragent not in last_call_dict:
                        last_call_dict[useragent] = {}  # Key - timestamps, value - last timestamp from that user

                    # Set next call as infinity. This won't be changed only for the last call from each user.
                    last_call_dict[useragent][timestamp] = float('inf')

                    # if old present
                    if useragent in previous_from_user:
                        # get old
                        previous_from_user = last_from_user[useragent]
                        # old -> new  map
                        last_call_dict[useragent][previous_from_user] = timestamp
                        # double check if entries are chronologically
                        if previous_from_user == timestamp:
                            log("Identical timestamps from one user")
                        if previous_from_user > timestamp:
                            log("Non chronological timestamps found")

                    # update old
                    last_from_user[useragent] = timestamp
    return last_call_dict


# def construct_start_dict(files):
#     start_dict = {}  # Key - useragent, value - list of start timestamps for that useragent
#     for file in files:
#         with open(file) as f:
#             for i, line in enumerate(f):
#                 json_line = json.loads(line)
#                 if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
#                     useragent = json_line['userAgent']
#                     timestamp = int(json_line['timestamp'])
#
#                     if useragent not in start_dict:
#                         start_dict[useragent] = []
#                     start_dict[useragent].append(timestamp)
#
#     for useragent in start_dict:
#         start_dict[useragent] = sorted(start_dict[useragent])
#
#     return start_dict

# def construct_concurrent_dict(files, start_dict, keep_alive):
def construct_concurrent_dict(files, last_call_dict, keep_alive):
    # parallelised = 0

    concurrent_dict = {}  # Key - timestamp, value - number of concurrent calls
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    useragent = json_line['userAgent']
                    timestamp = int(json_line['timestamp'])
                    elapsed_ms = int(json_line['elapsed_ms'])
                    end_timestamp = timestamp + elapsed_ms

                    upper_bound = min(
                        end_timestamp + keep_alive,
                        # next_useragent_timestamp(end_timestamp, useragent, start_dict)
                        last_call_dict[useragent][timestamp]
                    )

                    # if upper_bound != end_timestamp+keep_alive:
                    #     parallelised += 1

                    for stamp in range(timestamp, upper_bound+1):
                        if stamp not in concurrent_dict:
                            concurrent_dict[stamp] = 0
                        concurrent_dict[stamp] += 1
    # log("Parallel: "+str(parallelised))
    return concurrent_dict

def save_result(concurrent_dict, output_name):
    f = open(output_name, "w")
    for key in concurrent_dict:
        f.write(str(key) + ":" + str(concurrent_dict[key]) + "\n")
    f.close()

def keep_alive_estimates(file_paths, output_name, keep_alive):
    # start_dict = construct_start_dict(file_paths)
    # log("Start dict generated for " + str(file_paths))
    # concurrent_dict = construct_concurrent_dict(file_paths, start_dict, keep_alive)
    last_call_dict = construct_last_call_dict(file_paths)
    log("Last call dict constructed for " + str(file_paths))
    concurrent_dict = construct_concurrent_dict(file_paths, last_call_dict, keep_alive)
    log("Concurrent dict generated for " + str(file_paths))
    save_result(concurrent_dict, output_name)
    log("Results saved for " + str(file_paths))
