from Analyze import runAnalysis
import os

def download(serverName, fileName):
    os.system("cd alicdb1")
    os.system("wget " + serverName + str(fileName) + ".bz2")
    # os.system("bzip2 -d " + fileName)
    os.system("cd ..")
    os.system("cd alicdb2")
    os.system("wget " + serverName + str(fileName) + ".bz2")
    os.system("cd ..")
    # os.system("bzip2 -d " + fileName)

serverName = "http://alimonitor.cern.ch/download/michal/"
fileNames = ['http_access_log.json-20221120']
for name in fileNames:
    download(serverName, name)

# runAnalysis(fileNames)