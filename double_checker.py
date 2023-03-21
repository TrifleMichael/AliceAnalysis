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

def parse_files(files):
    concurrent_dict = {}  # Key - timestamp, value - number of concurrent calls
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                if i % 1000000 == 0:
                    log("Parsing progress in double_checker: " + str(i))
                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    timestamp = int(json_line['timestamp'])
                    elapsed_ms = int(json_line['elapsed_ms'])
                    end_timestamp = timestamp + elapsed_ms
                    for stamp in range(timestamp, end_timestamp+1):
                        if stamp not in concurrent_dict:
                            concurrent_dict[stamp] = 0
                        concurrent_dict[stamp] += 1
    return concurrent_dict

def save_result(concurrent_dict, output_name):
    f = open(output_name, "w")
    for key in concurrent_dict:
        f.write(str(key) + ":" + str(concurrent_dict[key]) + "\n")
    f.close()

def double_check(file_paths, output_name):
    concurrent_dict = parse_files(file_paths)
    log("Max for "+str(file_paths) + " is " + str(max(concurrent_dict.items())))
    save_result(concurrent_dict, output_name)
    log("Results saved for " + str(file_paths))
