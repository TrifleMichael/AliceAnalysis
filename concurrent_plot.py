import matplotlib.pyplot as plt
import os

input_path = "./keep_alive_estimates/"
output_path = "./concurrent_connections_plots/"
hours_per_ticks = 2

filenames = os.listdir(input_path)


for filename in filenames:
    print("Starting plot generation for "+filename)
    f = open(input_path+filename, "r")
    X = []
    Y = []
    for line in f:
        ind = int(line[:-1].split(":")[0])
        val = int(line[:-1].split(":")[1])
        X.append(ind)
        Y.append(val)
    f.close()
    print("File loaded")

    # compress_last = 720000
    compress_last = 10**5
    compression_counter = 0
    last_uncompressed = []

    compressed_X = []
    compressed_Y = []

    print("Starting compression")
    for i in range(len(X)):
        last_uncompressed.append(Y[i])
        if compression_counter == compress_last:
            compressed_X.append(i)
            compressed_Y.append(max(last_uncompressed))
            last_uncompressed = []
            compression_counter = 0
        compression_counter += 1

    # print("Creating plot")
    # plt.plot(compressed_X, compressed_Y)
    # output_formatted = output_path+filename+"_max_"+str(compress_last)+".png"
    # plt.savefig(output_formatted)
    # print("Plot created:", output_formatted)

    print("Creating plot")
    fig, ax = plt.subplots()
    ticks = [i*len(X)//compress_last//24*hours_per_ticks for i in range(24//hours_per_ticks)]
    ax.set_xticks(ticks)
    labels = [str(t*hours_per_ticks)+"h" for t in range(24//hours_per_ticks)]
    ax.set_xticklabels(labels)
    ax.plot(compressed_Y)
    output_formatted = output_path+filename+"_max_"+str(compress_last)+".png"
    plt.savefig(output_formatted)
    print("Plot created:", output_formatted)
