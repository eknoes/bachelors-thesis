import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from functools import reduce
import numpy as np

def get_interval_results(result, key):
    vars = list()
    for interval in result["intervals"]:
        vars.append(interval["streams"][0][key])

    return vars

def to_mega(value):
    return value / 10**6

def to_kilo(value):
    return value / 10**3

def average_intervals(intervals):
        average = list()

        for i in range(0, len(intervals[0])):
            sum = 0
            n = 0
            for j in range(0, len(intervals)):
                if i < len(intervals[j]):
                    sum += intervals[j][i]
                    n += 1
            average.append(sum / n)
        return average

def plot_average_interval(names, key, transform, label):
    lgd = list()
    for name in names:
        with open("raw/encrypted/"+ name[0] + "-iperf.json", "r") as file:
            iperf = json.load(file)
            all = list()

            for res in iperf:
                all.append(list(map(transform, get_interval_results(res, key))))

            lgd.append(plt.plot(average_intervals(all), label=name[1])[0])

    plt.legend(handles=lgd)

    plt.ylabel(label)
    plt.show()

def plot_bar(names, values, label):
    values = list()
    for name in names:
        with open("raw/encrypted/" + name[0] + "-iperf.json", "r") as f:
            iperf = json.load(f)
            dist = list()
            n = 0
            val = 0.0
            for result in iperf:
                if "error" in result.keys():
                    print("Failed run detected, ignoring")
                    continue

                val += to_mega(result["end"]["sum_received"]["bits_per_second"])
                n += 1
            val = val / n
            values.append(val)

    rtt = [list(),list(),list()]
    label = [range(3), range(3), range(3)]
    i = 0
    for val in zip(names, values):
            rtt[i%3].append(val[1])
            #label[i%3].append(val[0][1])
            i += 1

    fig, ax = plt.subplots()
    ax.yaxis.grid(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    colors = ['#AAAAAA'] + ['#777777'] +  ['#555555']
    for pos, val, shift, color in zip(label, rtt, range(0,3), colors):
        bars = ax.bar([p + shift*.25 for p in pos], val, 0.25)

        for patch1 in bars.patches:
            patch1.set_facecolor(color)
            patch1.zorder = 2
            patch1.set_edgecolor("#000000")

    ax.set_xticks([i+.25 for i in range(3)])
    ax.set_xticklabels(["MTU 1468", "MTU 1500", "MTU 2936"])

    eth = mpatches.Patch(color=colors[0], label='Ethernet')
    macsec = mpatches.Patch(color=colors[1], label='MACsec with Jumbo frames')
    proposal = mpatches.Patch(color=colors[2], label='MACsec with Fragmentation')
    plt.legend(handles=[eth,macsec,proposal], bbox_to_anchor=(0., -.15, 1., .102), loc=3, ncol=3, mode="expand", frameon=False)

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d+.05, +d+.05), **kwargs)        # top-left diagonal
    #ax.plot((1 - d, 1 + d), (-d+.05, +d+.05), **kwargs)  # top-right diagonal

    d = .015
    ax.plot((-d, +d), (-d+.03, +d+.03), **kwargs)        # top-left diagonal
    #ax.plot((1 - d, 1 + d), (-d+.03, +d+.03), **kwargs)  # top-right diagonal

    return fig, ax

def plot_iperf_distribution(names, key, transform):
    data = [list(), list(), list()]
    labels = [range(1,4), range(1,4), range(1,4)]
    i = 0
    for name in names:
        with open("raw/encrypted/" + name[0] + "-iperf.json", "r") as f:
            iperf = json.load(f)
            dist = list()
            for result in iperf:
                if "error" in result.keys():
                    print("Failed run detected, ignoring")
                    continue

                val = transform(key(result))
                dist.append(val)
            dist.sort()

            a = np.array(dist)
            print(name[1].replace("\n", " ") + " & " + str(round(np.percentile(a, 25), 2)) + " & " + str(round(np.percentile(a, 50), 2)) + " & " + str(round(np.percentile(a, 75), 2)) + "\\\\")
            data[i%3].append(dist)
            i += 1

    fig, ax= plt.subplots()
    ax.yaxis.grid(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    colors = ['#AAAAAA'] + ['#777777'] +  ['#555555']
    for pos, val, shift, color in zip(labels, data, range(0,3), colors):
        box = ax.boxplot(val, positions=[p + shift*.25 for p in pos], sym="", whis=[3,97], patch_artist=True, widths=(.25, .25, .25),manage_xticks=False)
        for patch1 in box['boxes']:
            patch1.set_facecolor(color)
        plt.setp(box["medians"], color="#000000")

    ax.set_xticks([i+.25 for i in range(1,4)])
    ax.set_xticklabels(["MTU 1468", "MTU 1500", "MTU 2936"])


    eth = mpatches.Patch(color=colors[0], label='Ethernet')
    macsec = mpatches.Patch(color=colors[1], label='MACsec with Jumbo frames')
    proposal = mpatches.Patch(color=colors[2], label='MACsec with Fragmentation')
    plt.legend(handles=[eth,macsec,proposal], bbox_to_anchor=(0., -.15, 1., .102), loc=3, ncol=3, mode="expand", frameon=False)

    return fig, ax

classes = [("no-macsec-1468", "Ethernet\nMTU 1468"), ("orig-1468", "MACsec\nMTU 1468"), ("frag-1468", "Proposal\nMTU 1468"), ("no-macsec-1500", "Ethernet\nMTU 1500"), ("orig-jumbo-1500", "MACsec\nMTU 1500"), ("frag-1500", "Proposal\nMTU 1500"),  ("no-macsec-2936", "Ethernet\nMTU 2936"), ("orig-jumbo-2936", "MACsec\nMTU 2936"),  ("frag-2936", "Proposal\nMTU 2936")]

#plot_iperf_distribution(classes, lambda x: x["end"]["sum_received"]["bits_per_second"], to_mega, "Mbit/s", "Bandwith")

print("Bandwidth")
fig, ax1 = plot_iperf_distribution(classes, lambda x: x["end"]["sum_received"]["bits_per_second"], to_mega)
ax1.set_yticks(range(300,1300,200))
fig.text(0.06, 0.5, 'Sent bytes / CPU Utilization in %', ha='center', va='center', rotation='vertical')

fig.set_size_inches(10,5)
plt.savefig('../thesis/figures/cpu-bandwidth-boxplot.svg', bbox_inches='tight', dpi=300)
plt.clf()

print("Bandwidth")
fig, ax1 = plot_bar(classes, [929.30, 907.51, 907.51, 930.69, 909.03, 864.19, 962.48, 950.05,  924.90], "Bandwith")
fig.text(0.06, 0.5, 'Bandwidth in Mbit/s', ha='center', va='center', rotation='vertical')
#plt.subplots_adjust(hspace=0.05)
ax1.set_ylim(800, 980)
ax1.set_yticks(range(820,980,20))

#ax2.set_ylim(0,60)
#ax2.set_yticks(range(0,60,20))

fig.set_size_inches(10,6)
plt.savefig('../thesis/figures/bandwidth-bar.svg', bbox_inches='tight', dpi=300)
plt.clf()

print("Megabytes / CPU")
fig, ax1 = plot_iperf_distribution(classes, lambda x: to_mega(x["end"]["sum_sent"]["bytes"])/x["end"]["cpu_utilization_percent"]["host_total"], float)
ax1.set_yticks(range(300,1300,200))
fig.text(0.06, 0.5, 'Sent MB / CPU Utilization in %', ha='center', va='center', rotation='vertical')

fig.set_size_inches(10,5)
plt.savefig('../thesis/figures/cpu-bandwidth-boxplot.svg', bbox_inches='tight', dpi=300)
plt.clf()

print("CPU")
fig, ax = plot_iperf_distribution(classes, lambda x: x["end"]["cpu_utilization_percent"]["host_total"], float)
ax.set_yticks(range(0,6,1))
ax.set_ylim(0, 6)
plt.ylabel("Sender CPU Utilization in %")
fig.set_size_inches(10,5)
plt.savefig('../thesis/figures/cpu-usage-boxplot.svg', bbox_inches='tight', dpi=300)
plt.clf()
