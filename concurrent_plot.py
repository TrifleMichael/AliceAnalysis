import matplotlib.pyplot as plt
import os

# Tworzy wykresy liczby polaczen na przestrzeni czasu na podstawie danych z keep_alive_estimates albo no_keep_alives

# input_path = "./keep_alive_estimates/"
# output_path = "./keep_alive_estimates_plots/"

input_path = "./no_keepalives/"
output_path = "./no_keepalives_plots/"

hours_per_ticks = 2

filenames = os.listdir(input_path)


for filename in filenames:
    compress_last = 600000
    output_formatted = output_path+filename+"_max_"+str(compress_last)+".png"
    if not os.path.isfile(output_formatted):
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

        compression_counter = 0
        last_uncompressed = []

        compressed_X = []
        compressed_Y = []

        print("Starting compression")
        for i in range(len(X)):
            last_uncompressed.append(Y[i])
            compression_counter += 1
            if compression_counter == compress_last:
                compressed_X.append(i)
                compressed_Y.append(int(sum(last_uncompressed)/len(last_uncompressed))) # TODO: SHOULD BE MAX
                last_uncompressed = []
                compression_counter = 0

        print("Creating plot")
        fig, ax = plt.subplots()
        ticks = [i*len(X)/compress_last/24*hours_per_ticks for i in range(24//hours_per_ticks)]
        ax.set_xticks(ticks)
        labels = [str(t*hours_per_ticks)+"h" for t in range(24//hours_per_ticks)]
        ax.set_xticklabels(labels)
        ax.plot(compressed_Y)

        ax.grid(True)
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Concurrent calls (max from last ' + str(compress_last//60000) + ' min)')
        keep_alive = filename.split("_")[0]
        ax.set_title('Keep-alive: '+str(keep_alive))  # TODO: ADD DATE TO TITLE

        plt.savefig(output_formatted, dpi=300)
        print("Plot created:", output_formatted)
    else:
        print("Skipping plot for", output_formatted)
