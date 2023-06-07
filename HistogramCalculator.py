import os

# Tworzy plik opisujacy histogram czasu polaczen

fileNames = [
    "http_access_log.json-20230524",
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