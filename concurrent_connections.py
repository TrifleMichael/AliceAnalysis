import matplotlib.pyplot as plt
import os

from open_window_analysis import log


def concurrentConnections(file_path):
    f = open(file_path, "r")
    values = []
    for line in f:
        values.append(int(line[:-1]))
    f.close()
    plt.plot(values)
    # plt.show()
    plt.savefig("plot")

def max_from_last_n_connections(n, file_path, output_name, hours_per_ticks=2):
    max_vals = []
    last_vals = []
    line_number = 0

    f = open(file_path, "r")
    for line in f:
        line_number += 1
        val = int(line[:-1])
        last_vals.append(val)
        if len(last_vals) == n:
            max_vals.append(max(last_vals))
            last_vals = []
    f.close()

    if len(last_vals) > 0:
        max_vals.append(max(last_vals))

    fig, ax = plt.subplots()
    ticks = [i*line_number//n//24*hours_per_ticks for i in range(24//hours_per_ticks)]
    ax.set_xticks(ticks)
    labels = [str(t*hours_per_ticks)+"h" for t in range(24//hours_per_ticks)]
    ax.set_xticklabels(labels)
    ax.plot(max_vals)
    plt.savefig(output_name+"_max_"+str(n)+".png")
    print("Done " + output_name+"_max_"+str(n)+".png")


# concurrentConnections("100_20221120")
# maxs = [10**i for i in range(4, 7)]
# names = ["20221101", "20221112", "20221116", "20221121"]
# try:
maxs = [10**5]
output_path = "./concurrent_connections_plots/"
names = os.listdir(output_path)

current = 0
all = len(names) * len(maxs)

for name in names:
    for m in maxs:
        max_from_last_n_connections(m, "./output/" + name, output_path+name)
        current += 1
        log("Done "+str(current)+" out of "+str(all))

# except Exception as e:
#     log("Terrible exception occured:")
#     log(repr(e))


