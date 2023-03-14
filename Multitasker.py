import os

from Analyze import generateDiffFiles
from open_window_analysis import generateConnectionsGraph
from datetime import datetime

def log(information):
    f = open("LOGS", "a")
    f.write(str(datetime.now()))
    f.write(" : ")
    f.write(information)
    f.write("\n")
    f.close()
    print(information)

def download(serverName, fileName, prefixes):
    for prefix in prefixes:
        if not os.path.isfile(prefix+fileName):  # If file is not present
            if not os.path.isfile(prefix + fileName + ".bz2"):  # If archive is not present
                print("Downloading", prefix+fileName)
                os.system("wget " + serverName + prefix + fileName + ".bz2")  # Download archive
                os.system("mv " + fileName + ".bz2 " + prefix+fileName + ".bz2")  # Move the archive to the destination
            print("Unpacking", prefix+fileName)
            os.system("bzip2 -cd " + prefix+fileName+".bz2 > "+prefix+fileName)  # Unpack the archive in destination

def remove(fileName, prefixes):
    for prefix in prefixes:
        os.system("rm " + prefix + fileName)
        os.system("rm " + prefix + fileName + ".bz2")

prefixes = ["alicdb1/", "alicdb2/"]
serverName = "http://alimonitor.cern.ch/download/michal/"
fileNames = ['http_access_log.json-20221102']

# fileNames = [
#     "http_access_log.json-20221116",
#     "http_access_log.json-20221121",
#     "http_access_log.json-20221112",
#     "http_access_log.json-20221101",
#     "http_access_log.json-20221113",
#     "http_access_log.json-20221118",
#     "http_access_log.json-20221103",
#     "http_access_log.json-20221117",
#     "http_access_log.json-20221107",
#     "http_access_log.json-20221111",
#     "http_access_log.json-20221123",
#     "http_access_log.json-20221119",
#     "http_access_log.json-20221110",
#     "http_access_log.json-20221109",
#     "http_access_log.json-20221105",
#     "http_access_log.json-20221104",
#     "http_access_log.json-20221126",
#     "http_access_log.json-20221128",
#     "http_access_log.json-20221106",
#     "http_access_log.json-20221114",
#     "http_access_log.json-20221127",
#     "http_access_log.json-20221115",
#     "http_access_log.json-20221108",
#     "http_access_log.json-20221124",
#     "http_access_log.json-20221122",
#     "http_access_log.json-20221125",
#     "http_access_log.json-20221102",
#     "http_access_log.json-20221120"
# ]

# for name in fileNames:
#     if not os.path.isfile("diff_files/diffs_"+name):
#         download(serverName, name, prefixes)
#         generateDiffFiles(name, prefixes)
#         remove(name, prefixes)

window_sizes = [100]
for name in fileNames:
    for size in window_sizes:
        outputName = str(size) + "_" + name + ".png"
        if not os.path.isfile(outputName):
            log("Starting download for: "+name)
            download(serverName, name, prefixes)
            log("Preparing graph for: "+name)
            generateConnectionsGraph([prefixes[0] + name, prefixes[1] + name], outputName, size)
            # remove(name, prefixes)
        else:
            log("Skipping task for "+outputName)
