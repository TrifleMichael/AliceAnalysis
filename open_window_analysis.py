import json
import matplotlib.pyplot as plt

from collections import defaultdict
from typing import List
from copy import deepcopy
from datetime import datetime
# path = "data/dir1/http_access_log.json-20221103"

def log(information):
    f = open("LOGS", "a")
    f.write(str(datetime.now()))
    f.write(" WA : ")
    f.write(information)
    f.write("\n")
    f.close()
    print(information)

class Event:
    def __init__(self, timestamp, event_type):
        self.timestamp = timestamp
        self.event_type = event_type

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __repr__(self):
        return f"{self.timestamp}"


class Record:
    def __init__(self, start_timestamp: int, end_timestamp: int):
        self.start_event = Event(start_timestamp, "start")
        self.end_event = Event(end_timestamp, "end")

    def __lt__(self, other):
        return self.start_event < other.start_event

    def __repr__(self):
        return f"({self.start_event}, {self.end_event})"


def parse_file(files):
    user_agent_dict = defaultdict(list)
    for file in files:
        with open(file) as f:
            for i, line in enumerate(f):
                if i % 10e6 == 0:
                    print(i)

                json_line = json.loads(line)
                if 'userAgent' in json_line and 'timestamp' in json_line and 'elapsed_ms' in json_line:
                    user_agent = json_line['userAgent']
                    timestamp = int(json_line['timestamp'])
                    elapsed_ms = int(json_line['elapsed_ms'])
                    end_timestamp = timestamp + elapsed_ms
                    user_agent_dict[user_agent].append(Record(timestamp, end_timestamp))
    return user_agent_dict


def find_minimum_of_dict(dictionary):
    return min(min(timestamps) for timestamps in dictionary.values())


def find_maximum_of_dict(dictionary):
    return max(max(timestamps) for timestamps in dictionary.values())


def merge_records_list(records_list):
    min_start_timestamp = min(record.start_event.timestamp for record in records_list)
    max_end_timestamp = max(record.end_event.timestamp for record in records_list)
    return Record(min_start_timestamp, max_end_timestamp)


def merge_agent_records(user_records):
    if len(user_records) == 1:
        return user_records
    records_to_merge = []
    result_records = []
    for i in range(len(user_records) - 1):
        curr_record = user_records[i]
        next_record = user_records[i + 1]
        # dodajemy zawsze, bo najwyzej do funkcji przekazemy liste z jednym elementem i to jest ok
        records_to_merge.append(curr_record)
        # resetujemy liste jezeli jest przerwa miedzy interwalami
        if curr_record.end_event < next_record.start_event:
            if i > 1 and i == len(user_records) - 2:
                records_to_merge.append(next_record)
            merged_record = merge_records_list(records_to_merge)
            result_records.append(merged_record)
            records_to_merge = []
        else:
            if i == len(user_records) - 2:
                records_to_merge.append(next_record)
                merged_record = merge_records_list(records_to_merge)
                result_records.append(merged_record)
    if user_records[-1].start_event > result_records[-1].end_event:
        result_records.append(user_records[-1])
    return result_records


def merge_records_in_dict(agent_dict):
    for agent, records in agent_dict.items():
        merged_records = merge_agent_records(records)
        agent_dict[agent] = merged_records


def analyze_number_of_connections(agent_dict):
    all_records = []
    for agent_records in agent_dict.values():
        all_records += agent_records
    all_events = []
    for record in all_records:
        all_events.append(record.start_event)
        all_events.append(record.end_event)
    all_events.sort()
    connections_at_time = [0]
    curr_timestamp = all_events[0].timestamp
    log("All events appended")
    for event in all_events:
        if event.timestamp != curr_timestamp:
            for i in range(event.timestamp - curr_timestamp):
                connections_at_time.append(connections_at_time[-1])
            curr_timestamp = event.timestamp
        if event.event_type == "start":
            connections_at_time[-1] += 1
        elif event.event_type == "end":
            connections_at_time[-1] -= 1
    return connections_at_time


def add_window_length(agent_dict, window_size):
    new_agent_dict = agent_dict.copy()
    for agent, records in new_agent_dict.items():
        for record in records:
            record.end_event.timestamp += window_size
    return new_agent_dict


def sort_all_agent_records(user_agent_dict):
    for user, records in user_agent_dict.items():
        user_agent_dict[user] = sorted(records)


def save_results(results, outputName):
    f = open(outputName + "_results", "w")
    for result in results:
        f.write(result)
        f.write("\n")
    f.close()

def compress_results(results, skips_per_step):
    compressed = []
    last_max = 0
    for i, result in enumerate(results):
        if (i + 1) % skips_per_step == 0:
            compressed.append(last_max)
            last_max = 0
        last_max= max(result, last_max)
    return compressed

def generateConnectionsGraph(files, outputName, window_size):
    try:
        log("Starting window analysis for " + str(outputName))
        user_agent_dict = parse_file(files)
        log("File parsed")
        sort_all_agent_records(user_agent_dict)
        log("Containers sorted")
        curr_agent_dict = add_window_length(user_agent_dict, window_size)
        log("Windows added")
        merge_records_in_dict(curr_agent_dict)
        log("Records merged")
        result_list = analyze_number_of_connections(curr_agent_dict)
        log("Connections calculated")
        save_results(result_list, outputName)
        log("Results saved")
        compressed_results = compress_results(result_list, 100)
        log("Compressed results")
        plt.bar(list(range(len(compressed_results))), result_list)
        log("Plot prepared")
        # plt.show()
        plt.savefig(outputName)
        log("Output file saved")
    except Exception as ex:
        log("Terrible error took place: " + ex.__str__())
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        log(message)

