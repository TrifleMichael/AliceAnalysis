import os
import traceback

from Analyze import generateDiffFiles
from double_checker import double_check
from open_window_analysis import generateConnectionsGraph
from datetime import datetime
from open_window_analysis import log


def download(serverName, fileName, prefixes):
    for prefix in prefixes:
        if not os.path.isfile(prefix + fileName + ".bz2"):  # If archive is not present
            if not os.path.isfile(prefix + fileName):  # If file is not present
                log("Downloading " + serverName + prefix + fileName + ".bz2")
                os.system("wget " + serverName + prefix + fileName + ".bz2")  # Download archive
                os.system(
                    "mv " + fileName + ".bz2 " + prefix + fileName + ".bz2")  # Move the archive to the destination
            else:
                log("Skipping download for "+fileName)
            print("Unpacking", prefix + fileName)
            os.system(
                "bzip2 -cd " + prefix + fileName + ".bz2 > " + prefix + fileName)  # Unpack the archive in destination
        else:
            log("Skipping unpacking for ")


def remove(fileName, prefixes):
    for prefix in prefixes:
        os.system("rm " + prefix + fileName)
        os.system("rm " + prefix + fileName + ".bz2")


prefixes = ["alicdb1/", "alicdb2/"]
serverName = "http://alimonitor.cern.ch/download/michal/"

fileNames = [
    # "http_access_log.json-20230312",
    # "http_access_log.json-20230313",
    "http_access_log.json-20230314"
]



def connection_time_analysis(fileNames):
    for name in fileNames:
        if not os.path.isfile("diff_files/diffs_" + name):
            download(serverName, name, prefixes)
            generateDiffFiles(name, prefixes)
            remove(name, prefixes)


# try:
#     window_sizes = [100]
#     for name in fileNames:
#         for size in window_sizes:
#             outputName = str(size) + "_" + name + ".png"
#             if not os.path.isfile("./output/" + outputName + "_results"):
#                 log("Considering download for: " + name)
#                 download(serverName, name, prefixes)
#                 log("Preparing graph for: " + name)
#                 generateConnectionsGraph([prefixes[0] + name, prefixes[1] + name], outputName, size)
#                 remove(name, prefixes)
#             else:
#                 log("Skipping task for " + outputName)
#
# except Exception as ex:
#     log("Error took place: " + ex.__str__())
#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#     message = template.format(type(ex).__name__, ex.args)
#     log(message)
#     print(traceback.format_exc())

# def download_fix():
#     path1 = "http://alimonitor.cern.ch/download/michal/alicdb1/http_access_log.json-20230314.bz2"
#     name1 =
#     path2 = "http://alimonitor.cern.ch/download/michal/alicdb2/http_access_log-20230314.bz2"
#     name2 =
#
#     def download_single(download_path, name):
#         log("Downloading " + download_path)
#         os.system("wget " + download_path)  # Download archive
#         os.system("mv " + name + "")
#         log("Unpacking " + name)
#         os.system("bzip2 -cd " + name + " > " + name.replace(".bz2", ""))  # Unpack the archive in destination
#         log("Unpacked " + name.replace(".bz2", ""))
#
#     download_single(name1)
#     download_single(name2)

try:
    inputName = "http_access_log.json-20221101"
    outputName = "20221101_double_checked"
    # if not os.path.isfile("./double_check_output/" + outputName):
        # download_fix()
        # log("Starting double checker for: " + inputName)
    double_check(["alicdb1/"+inputName, "alicdb2/"+inputName], outputName)
    # else:
    #     log("Skipping task for " + outputName)

except Exception as ex:
    log("Error took place: " + ex.__str__())
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    log(message)
    print(traceback.format_exc())