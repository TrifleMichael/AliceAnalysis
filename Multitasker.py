import os

from Analyze import generateDiffFiles


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

prefixes = ["alicdb1/", "alicdb2/"]
serverName = "http://alimonitor.cern.ch/download/michal/"
fileNames = ['http_access_log.json-20221120']

for name in fileNames:
    if not os.path.isfile("./diffs_"+name):
        download(serverName, name, prefixes)
        generateDiffFiles(name, prefixes)
        remove(name, prefixes)
