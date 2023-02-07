import json

userAgentDict = {}


class Record:
    def __init__(self, timestamp, elapsed_ms):
        self.timestamp = timestamp
        self.elapsed_ms = elapsed_ms


def sortUserAgentBucket(arr):
    span = int(len(arr) / 1.3)
    while span >= 1:
        i = 0
        while i + span < len(arr):
            if arr[i].timestamp > arr[i + span].timestamp:
                arr[i], arr[i + span] = arr[i + span], arr[i]
            i += 1
        span = int(span / 1.3)


f = open('http_access_log.json-20221120(1)', 'r')
for i, line in enumerate(f):
    if i % 10e6 == 0:
        print(i)

    jsonLine = json.loads(line)
    if True or 'dn' in jsonLine:  # HACK TO MAKE IT ACCEPT REGARDLESS OF DNS
        if 'userAgent' in jsonLine and 'timestamp' in jsonLine and 'elapsed_ms' in jsonLine:
            userAgent = jsonLine['userAgent']
            if userAgent not in userAgentDict:
                userAgentDict[userAgent] = []
            userAgentDict[userAgent].append(Record(jsonLine['timestamp'], jsonLine['elapsed_ms']))
f.close()

# f = open('http_access_log.json-alicdb2-20221115', 'r')
# for i, line in enumerate(f):
#     if i % 10e6 == 0:
#         print(i)
#
#     jsonLine = json.loads(line)
#     if 'dn' in jsonLine:
#         if 'userAgent' in jsonLine and 'timestamp' in jsonLine and 'elapsed_ms' in jsonLine:
#             userAgent = jsonLine['userAgent']
#             if userAgent not in userAgentDict:
#                 userAgentDict[userAgent] = []
#             userAgentDict[userAgent].append(Record(jsonLine['timestamp'], jsonLine['elapsed_ms']))
# f.close()

print("Reading complete")

for i in userAgentDict:
    sortUserAgentBucket(userAgentDict[i])

print("User agent containers sorted")

zero_diff = 0
one_diff = 0
large_diff = 0
for i in userAgentDict:
    for j in range(1, len(userAgentDict[i])):
        if userAgentDict[i][j].timestamp < userAgentDict[i][j - 1].timestamp:
            print("ERROR IN SORTING")
            exit()

        diff = int(userAgentDict[i][j].timestamp) - int(float(userAgentDict[i][j].elapsed_ms)) - int(userAgentDict[i][j - 1].timestamp)

        if diff == 0:
            zero_diff += 1
        elif diff == -1:
            one_diff += 1
        elif diff < -1:
            large_diff += 1

print(zero_diff, one_diff, large_diff)
print(zero_diff + one_diff + large_diff)

print("Check complete")

# out = open('out.txt', 'w')
# for i in userAgentDict:
#     for j in range(len(userAgentDict[i])):
#         out.write(str(i) + "!" + str(userAgentDict[i][j].timestamp) + "!" + str(userAgentDict[i][j].elapsed_ms) + "\n")
# out.close()
#
# print("Results saved")
