import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

# from multiprocessing import Pool
# def get_timestamp_dict(sub_name):
#     f = open(sub_name, "r")
#     for i, line in enumerate(f):
#         # if i == 10*60*1000*4: #TODO REMOVE
#         #     break
#         if i % 1000000 == 0:
#             print(str(i//1000000) + "mln")
#         json_line = json.loads(line)
#         if 'timestamp' in json_line and 'elapsed_ms' in json_line:
#             timestamp = int(json_line['timestamp'])
#             if timestamp not in timestamp_dict:
#                 timestamp_dict[timestamp] = 0
#             timestamp_dict[timestamp] += 1
#     f.close()
#     return timestamp_dict

# def merge_dicts(dict1, dict2):


# names = os.listdir("alicdb1")
names = ["http_access_log.json-20230524"]

for name in names:
    print("Starting analysis for", name)
    timestamp_dict = {}
    sub_names = ["alicdb1/"+name] #  , "alicdb2/"+name

    for sub_name in sub_names:
        f = open(sub_name, "r")
        for i, line in enumerate(f):
            if i % 1000000 == 0:
                print(str(i//1000000) + "mln")
            json_line = json.loads(line)
            if 'timestamp' in json_line:
                timestamp = int(json_line['timestamp'])
                if timestamp not in timestamp_dict:
                    timestamp_dict[timestamp] = 0
                timestamp_dict[timestamp] += 1
        f.close()
        print("Finished reading", sub_name)

    min_timestamp = min(timestamp_dict)
    max_timestamp = max(timestamp_dict)
    print("MIN:", datetime.fromtimestamp(min_timestamp//1000))
    print("MAX:", datetime.fromtimestamp(max_timestamp//1000))
    print("min_timestamp:", min_timestamp, "min_timestamp//1000", min_timestamp//1000)

    values = []
    starts = []
    for start in range(min_timestamp, max_timestamp+1, 10*60*1000): # 10 minute steps
        values.append(0)
        starts.append(start)
        for timestamp in range(start, min(start+1000, max_timestamp)): # 1 second interval
            if timestamp in timestamp_dict:
                values[-1] += timestamp_dict[timestamp]

    # for i, val in enumerate(values):
    #     print(i, val)

    tick_num = 12
    fig, ax = plt.subplots()
    ticks = [i for i in range(0, len(starts), tick_num)]
    ax.set_xticks(ticks)
    labels = [str(datetime.fromtimestamp(starts[i]//1000)) for i in range(0, len(starts), tick_num)]
    ax.set_xticklabels(labels)
    ax.plot(values)

    ax.grid(True)
    ax.set_xlabel('Time')
    ax.set_ylabel("Timestamps / s")
    ax.set_title("Requests per second over time (alicdb1 only)") 
    plt.plot(values)
    plt.show()


    