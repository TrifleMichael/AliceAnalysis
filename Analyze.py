def generateDiffFiles(fileName, prefixes):

    import json
    userAgentDict = {}

    raportFile = open("raport", "a")
    raportFile.write("Starting a new download for " + fileName + "\n")

    class Record:
        def __init__(self, timestamp, elapsed_ms):
            self.timestamp = timestamp
            self.elapsed_ms = elapsed_ms

    # Load files into memory
    for prefix in prefixes:
        f = open(prefix+fileName, 'r')
        for i, line in enumerate(f):
            if i % 10e6 == 0:
                raportFile.write(str(i) + "\n")
                print(i)

            jsonLine = json.loads(line)
            if 'userAgent' in jsonLine and 'timestamp' in jsonLine and 'elapsed_ms' in jsonLine:
                userAgent = jsonLine['userAgent']
                if userAgent not in userAgentDict:
                    userAgentDict[userAgent] = []
                userAgentDict[userAgent].append(Record(jsonLine['timestamp'], jsonLine['elapsed_ms']))
        f.close()

    raportFile.write("Reading complete\n")
    print("Reading complete")

    for i in userAgentDict:
        userAgentDict[i].sort(key=lambda x: x.timestamp)

    raportFile.write("User agent containers sorted\n")
    print("User agent containers sorted")

    d = open("diff_files/diffs_" + fileName, "w")

    for i in userAgentDict:
        d.write("!" + i + "\n")
        for j in range(1, len(userAgentDict[i])):
            if userAgentDict[i][j].timestamp < userAgentDict[i][j - 1].timestamp:
                raportFile.write("ERROR IN SORTING\n")
                print("ERROR IN SORTING")
                exit()

            diff = int(userAgentDict[i][j].timestamp) - int(float(userAgentDict[i][j - 1].elapsed_ms)) - int(userAgentDict[i][j - 1].timestamp)
            d.write(str(diff) + "\n")

    d.close()

    print("Check complete")
    raportFile.write("Check complete\n")
    raportFile.close()

