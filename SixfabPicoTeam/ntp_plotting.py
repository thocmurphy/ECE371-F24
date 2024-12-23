# This file is used to plot all of the data from running the ntp_drift.py script

import matplotlib.pyplot as plt

raw_data = ['test1_raw.txt', 'test2_raw.txt']
servers = ['pool.ntp.org', 'time1.google.com']

def plot_data(time, data, name):
    plt.plot(time, data, label=name)
    
    plt.xlabel('Time (minutes)')
    plt.ylabel('Drift (ms)')
    plt.title('Plotting Drift on %s'%(server))
    plt.legend()
    plt.show()

for i in range(len(raw_data)):
    data = []
    file = raw_data[i]
    server = servers[i]
    time = []
    with open(file, 'r') as f:
        for line in f:
            drift = line.split(', ')[2]
            if drift == 'Difference\n':
                continue
            print(int(drift))
            data.append(int(drift))
    for j in range(len(data)):
        time.append(j*5)
    plot_data(time, data, server)