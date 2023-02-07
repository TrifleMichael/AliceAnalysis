from Analyze import runAnalysis
import os

def download(serverName, fileName):
    os.system("wget -o alicdb1/"+fileName+".bz2 " + serverName + "alicdb1/" + str(fileName) + ".bz2")
    # os.system("bzip2 -d " + fileName)
    os.system("wget -o alicdb2/"+fileName+".bz2 " + serverName + "alicdb2/" + str(fileName) + ".bz2")
    # os.system("bzip2 -d " + fileName)

serverName = "http://alimonitor.cern.ch/download/michal/"
fileNames = ['http_access_log.json-20221120']
for name in fileNames:
    download(serverName, name)

# runAnalysis(fileNames)