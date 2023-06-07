import os
import traceback

from keep_alive_estimates import keep_alive_estimates
from datetime import datetime

from no_keepalives import no_keepalive

# nohup python Multitasker.py &
# ps aux --headers | head -n 1 ; ps aux --headers | grep "mtrzeb"     <- wypisuje wszystkie procesy ktore naleza do mtrzeb (z kazdej sesji)

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
        if not os.path.isfile(prefix + fileName):  # If file is not present
            if not os.path.isfile(prefix + fileName + ".bz2"):  # If archive is not present 
                log("Downloading " + serverName + prefix + fileName + ".bz2")
                os.system("wget " + serverName + prefix + fileName + ".bz2")  # Download archive
                os.system(
                    "mv " + fileName + ".bz2 " + prefix + fileName + ".bz2")  # Move the archive to the destination
            else:
                log("Skipping download for "+fileName)
            log("Unpacking " + prefix + fileName)
            os.system(
                "bzip2 -cd " + prefix + fileName + ".bz2 > " + prefix + fileName)  # Unpack the archive in destination
        else:
            log("Skipping unpacking for "+prefix+fileName)


def remove(fileName, prefixes):
    for prefix in prefixes:
        os.system("rm " + prefix + fileName)
        os.system("rm " + prefix + fileName + ".bz2")


prefixes = ["alicdb1/", "alicdb2/"]
serverName = "http://alimonitor.cern.ch/download/michal/"
fileNames = ['http_access_log.json-20230524'] # , 'http_access_log.json-20230525'

# fileNames = [
#     "http_access_log.json-20230312",
#     "http_access_log.json-20230313",
#     "http_access_log.json-20230314",
#     "http_access_log.json-20230319",
#     "http_access_log.json-20230320",
#     "http_access_log.json-20230321"
# ]


## NO KEEPALIVES
try:
    for name in fileNames:
        outputName = "no_keepalives/" + "0_" + name
        if not os.path.isfile(outputName + "_results"):
            log("Considering download for: " + name)
            download(serverName, name, prefixes)
            log("Preparing graph for: " + name)
            no_keepalive([prefixes[0] + name, prefixes[1] + name], outputName)
            # remove(name, prefixes)
        else:
            log("Skipping task for " + outputName)

# KEEPALIVE ESTIMATES
# try:
#     keep_alive_times = [0]
#     for name in fileNames:
#         for keep_alive in keep_alive_times:
#             output_path = "./keep_alive_estimates/" + str(keep_alive) + "_" + name
#             if not os.path.isfile(output_path):
#                 download(serverName, name, prefixes)
#                 log("Starting keep alive estimate calculation: " + name + " with keep_alive " + str(keep_alive))
#                 keep_alive_estimates([prefixes[0] + name, prefixes[1] + name], output_path, keep_alive)
#                 # remove(name, prefixes)
#             else:
#                 log("Skipping task for " + output_path + " with keep_alive " + str(keep_alive))

# try:
#     for name in fileNames:
#         output_path = "./connection_starts/" + "starts_" + name
#         if not os.path.isfile(output_path):
#             download(serverName, name, prefixes)
#             calculate_start_of_connections([prefixes[0] + name, prefixes[1] + name], output_path)
#             # remove(name, prefixes)
#         else:
#             log("Skipping connection_starts for " + output_path)

except Exception as ex:
    log("Error took place: " + ex.__str__())
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    log(message)
    print(traceback.format_exc())