def runAnalysis(fileNames):

    import json
    userAgentDict = {}

    raportFile = open("raport", "w")

    class Record:
        def __init__(self, timestamp, elapsed_ms):
            self.timestamp = timestamp
            self.elapsed_ms = elapsed_ms


    # def sortUserAgentBucket(arr):
    #     span = int(len(arr) / 1.3)
    #     while span >= 1:
    #         i = 0
    #         while i + span < len(arr):
    #             if arr[i].timestamp > arr[i + span].timestamp:
    #                 arr[i], arr[i + span] = arr[i + span], arr[i]
    #             i += 1
    #         span = int(span / 1.3)

    for name in fileNames:
        f = open(name, 'r')
        for i, line in enumerate(f):
            if i % 10e6 == 0:
                raportFile.write(str(i) + "\n")
                print(i)

            jsonLine = json.loads(line)
            if True or 'dn' in jsonLine: # HACK
                if 'userAgent' in jsonLine and 'timestamp' in jsonLine and 'elapsed_ms' in jsonLine:
                    userAgent = jsonLine['userAgent']
                    if userAgent not in userAgentDict:
                        userAgentDict[userAgent] = []
                    userAgentDict[userAgent].append(Record(jsonLine['timestamp'], jsonLine['elapsed_ms']))
        f.close()

    raportFile.write("Reading complete\n")
    print("Reading complete")

    for i in userAgentDict:
        # sortUserAgentBucket(userAgentDict[i])
        userAgentDict[i].sort(key = lambda x: x.timestamp)

    raportFile.write("User agent containers sorted\n")
    print("User agent containers sorted")

    zero_diff = 0
    one_diff = 0
    large_diff = 0
    allDiffs = 0
    for i in userAgentDict:
        for j in range(1, len(userAgentDict[i])):
            if userAgentDict[i][j].timestamp < userAgentDict[i][j - 1].timestamp:
                raportFile.write("ERROR IN SORTING\n")
                print("ERROR IN SORTING")
                exit()

            diff = int(userAgentDict[i][j].timestamp) - int(float(userAgentDict[i][j - 1].elapsed_ms)) - int(userAgentDict[i][j - 1].timestamp)
            allDiffs += 1

            if diff == 0:
                zero_diff += 1
            elif diff == -1:
                one_diff += 1
            elif diff < -1:
                large_diff += 1

    print(allDiffs)
    print(zero_diff, one_diff, large_diff)
    print(zero_diff + one_diff + large_diff)
    raportFile.write("All diffs (including positive " + str(allDiffs))
    raportFile.write("Zero, one and large diff: " + str(zero_diff) + " " + str(one_diff) + " " + str(large_diff) + "\n")
    raportFile.write("Total diffs " + str(zero_diff + one_diff + large_diff))

    print("Check complete")
    raportFile.write("Check complete\n")
    raportFile.close()

    # out = open('out.txt', 'w')
    # for i in userAgentDict:
    #     for j in range(len(userAgentDict[i])):
    #         out.write(str(i) + "!" + str(userAgentDict[i][j].timestamp) + "!" + str(userAgentDict[i][j].elapsed_ms) + "\n")
    # out.close()
    #
    # print("Results saved")
