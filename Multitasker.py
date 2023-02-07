from Analyze import runAnalysis
import os

def download(serverName, fileName):
    os.system("cd db1")
    os.system("wget " + serverName + "alicdb1/" + str(fileName)) # Needs .bz2 at the end of filename
    # os.system("bzip2 -d " + fileName)
    os.system("cd ..")
    os.system("cd db2")
    os.system("wget " + serverName + "alicdb2/" + str(fileName))
    os.system("cd ..")
    # os.system("bzip2 -d " + fileName)

serverName = "http://alimonitor.cern.ch/download/michal/"


fileNames = ['db1/http_access_log.json-20221120']
runAnalysis(fileNames)
print("\n DB1 DONE\n")
fileNames = ['db2/http_access_log.json-20221120']
runAnalysis(fileNames)
print("\n DB2 DONE\n")