import csv
import matplotlib.pyplot as plt
import numpy as np


time = []
power = []
with open("data.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
    i = -1
    print("Reading...")
    for row in spamreader:
        i += 1
        if i == 0:
            continue
        time.append(i)
        power.append(row[2])
        if i > 86400:
            break

print("Plotting...")
plt.plot(time, power)
plt.xlabel("Time")
plt.ylabel("Power")
# plt.ylim([0,10])
plt.show()
