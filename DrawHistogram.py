import matplotlib.pyplot as plt

# STARY PLIK, NIE WIEM CZY DOBRZE DZIALA
# Tworzy histogram na podstawie danych z HistogramCalulator

fileNames = [
    "http_access_log.json-20221116",
    "http_access_log.json-20221121",
    "http_access_log.json-20221112",
    "http_access_log.json-20221101",
    "http_access_log.json-20221113",
    "http_access_log.json-20221118",
    "http_access_log.json-20221103",
    "http_access_log.json-20221117",
    "http_access_log.json-20221107",
    "http_access_log.json-20221111",
    "http_access_log.json-20221123",
    "http_access_log.json-20221119",
    "http_access_log.json-20221110",
    "http_access_log.json-20221109",
    "http_access_log.json-20221105",
    "http_access_log.json-20221104",
    "http_access_log.json-20221126",
    "http_access_log.json-20221128",
    "http_access_log.json-20221106",
    "http_access_log.json-20221114",
    "http_access_log.json-20221127",
    "http_access_log.json-20221115",
    "http_access_log.json-20221108",
    "http_access_log.json-20221124",
    "http_access_log.json-20221122",
    "http_access_log.json-20221125",
    "http_access_log.json-20221102",
    "http_access_log.json-20221120"
]

def drawHistogram(name):
    vals = []
    out = open("histogram_data/histogram_data_"+name, 'r')
    for i, line in enumerate(out):
        vals.append(int(line[:-1]))
    out.close()

    # x = [(str(20*i) + "ms") for i in range(len(vals))]
    x = []
    for i in range(len(vals)):
        if i % 5 == 0:
            x.append((str(20*i) + "ms"))
        else:
            x.append((i*" "))

    total = 0
    for i in range(len(vals)):
        total += vals[i]
        vals[i] = vals[i]/1000000
    print("Total values: ", total)

    fig, ax = plt.subplots()
    ax.bar(x, vals)
    ax.set_ylabel('Occurances (millions)')
    ax.set_xlabel('Intervals (each 20ms)')
    ax.grid()
    fig.set_size_inches(8, 6)

    # Save the histogram to a file
    plt.savefig("histograms/" + name + ".png")
    plt.close()


    # plt.bar(x, vals)
    # plt.ylabel('Occurances (millions)')
    # plt.xlabel('Intervals (each 20ms)')
    # plt.grid()
    #
    # fig = plt.gcf()
    # fig.set_size_inches(8, 6)
    # # plt.figure(figsize=(8, 6))
    # # plt.xlabel('Bin nr (20ms per bin)')
    # # plt.show()
    #
    # plt.savefig("histograms/"+name+".png")

for name in fileNames:
    drawHistogram(name)