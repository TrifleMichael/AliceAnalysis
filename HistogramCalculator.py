import os

fileNames = [
    "http_access_log.json-20221116",
    "http_access_log.json-20221121",
    "http_access_log.json-20221112",
    "http_access_log.json-20221101",
    "http_access_log.json-20221113",
    "http_access_log.json-20221118",
    "http_access_log.json-20221103",
    "http_access_log.json-20221117",
    "http_access_log.json-20221107",
    "http_access_log.json-20221111",
    "http_access_log.json-20221123",
    "http_access_log.json-20221119",
    "http_access_log.json-20221110",
    "http_access_log.json-20221109",
    "http_access_log.json-20221105",
    "http_access_log.json-20221104",
    "http_access_log.json-20221126",
    "http_access_log.json-20221128",
    "http_access_log.json-20221106",
    "http_access_log.json-20221114",
    "http_access_log.json-20221127",
    "http_access_log.json-20221115",
    "http_access_log.json-20221108",
    "http_access_log.json-20221124",
    "http_access_log.json-20221122",
    "http_access_log.json-20221125",
    "http_access_log.json-20221102",
    "http_access_log.json-20221120"
]

def calculateHistogram(fileName):

    BIN_NUM = 51
    cutoffDiff = 1000  # ms
    bins = [0 for _ in range(BIN_NUM)]

    f = open("diff_files/"+fileName, "r")
    for line in f:
        if line[0] != '!':
            diff = int(line[:-1])
            if diff < cutoffDiff:
                if diff < 0:
                    diff = 0
                bins[int(diff / cutoffDiff * (BIN_NUM - 1))] += 1
            else:
                bins[-1] += 1
    f.close()

    out = open("histogram_data/histogram_data_"+fileName, "w")
    for value in bins:
        out.write(str(value) + "\n")
    out.close()


for name in fileNames:
    if not os.path.isfile("histogram_data/histogram_data_"+name):
        calculateHistogram(name)