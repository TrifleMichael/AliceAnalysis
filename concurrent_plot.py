import matplotlib.pyplot as plt

f = open("downloaded/20221101_double_checked", "r")

X = []
Y = []
for line in f:
    val = int(line[:-1].split(":")[1])
    ind = int(line[:-1].split(":")[0])
    X.append(ind)
    Y.append(val)
f.close()

print("File loaded")
compress_last = 100000
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
        compression_counter = 0
        last_uncompressed = []
    compression_counter += 1

print("Creating plot")
plt.plot(compressed_X, compressed_Y)
plt.savefig("compressed_concurrent_plot_"+str(compress_last))
