import json
import matplotlib.pyplot as plt
from functools import reduce
import numpy as np
import matplotlib.patches as mpatches

def parse_ping(filename):
    with open(filename) as f:
        summary = False
        result = dict()
        items = list()
        for line in f:
            if line == "\n":
                continue

            if not summary:
                if line[0:4] == "PING":
                    # PING 1.1.1.2 (1.1.1.2) 1440(1468) bytes of data.
                    r = line.split(" ")
                    result["size"] = r[3].split("(")[:-1]
                    result["dest"] = r[1]
                elif line[0:3] == "---":
                    summary = True
                else:
                    # 1448 bytes from 1.1.1.2: icmp_seq=49972 ttl=64 time=0.169 ms
                    r = line.split(" ")
                    items.append((r[0], r[6].split("=")[1], r[7][:-2]))
            else:
                result["items"] = items

                if line[0:3] == "rtt":
                    # rtt min/avg/max/mdev = 0.117/0.153/0.408/0.015 ms, ipg/ewma 0.186/0.160 ms
                    r = line.split(" ")[3].split("/")
                    result["min"] = r[0]
                    result["avg"] = r[1]
                    result["max"] = r[2]
                else:
                    # 50000 packets transmitted, 50000 received, 0% packet loss, time 9325ms
                    r = line.split(" ")
                    result["count"] = r[0]
                    result["loss"] = r[5]
    return result

def plot_ping_boxplot(names, broken=True):
    data = [list(), list(), list()]
    labels = [range(1,4), range(1,4), range(1,4)]
    n = 0
    i = 0

    for name in names:
        ping = parse_ping("raw/encrypted/" + name[0] + "-ping.txt")
        val = list(map(lambda v: float(v[1]), ping['items']))

        data[i%3].append(val)
        n = ping["count"]

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



    return fig, ax

def create(names):
    colors = ['#AAAAAA'] + ['#777777'] +  ['#555555']
    eth = mpatches.Patch(color=colors[0], label='Ethernet')
    macsec = mpatches.Patch(color=colors[1], label='MACsec with Jumbo frames')
    proposal = mpatches.Patch(color=colors[2], label='MACsec with Fragmentation')

    # Zoomed one
    fig, ax = plot_ping_boxplot(names, broken=True)
    ax.set_yticks(np.arange(0.13,0.2,0.02))
    ax.set_ylim(0.12, 0.19)

    ax.arrow(3, 0.175, 0, 0.01, width=0.002, head_width=0.05, head_length=0.0025, color="#000000", zorder=2, capstyle="projecting")
    ax.arrow(3.25, 0.175, 0, 0.01, width=0.002, head_width=0.05, head_length=0.0025, color="#000000", zorder=2, capstyle="projecting")
    plt.legend(handles=[eth,macsec,proposal], bbox_to_anchor=(0., -.2, 1., .102), loc=3, ncol=3, mode="expand", frameon=False)

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d+.05, +d+.05), **kwargs)        # top-left diagonal
    #ax.plot((1 - d, 1 + d), (-d+.05, +d+.05), **kwargs)  # top-right diagonal

    d = .015
    ax.plot((-d, +d), (-d+.03, +d+.03), **kwargs)        # top-left diagonal
    #ax.plot((1 - d, 1 + d), (-d+.03, +d+.03), **kwargs)  # top-right diagonal

    fig.set_size_inches(10,4)
    plt.savefig('../thesis/figures/rtt-boxplot-zoom.svg', bbox_inches='tight', dpi=300)
    plt.clf()

    fig, ax = plot_ping_boxplot(names, broken=False)
    ax.set_yticks(np.arange(0.0,0.65,0.05))
    ax.set_ylim(0.0, 0.65)

    plt.legend(handles=[eth,macsec,proposal], bbox_to_anchor=(0., -.15, 1., .102), loc=3, ncol=3, mode="expand", frameon=False)

    fig.set_size_inches(10,6)
    plt.savefig('../thesis/figures/rtt-boxplot.svg', bbox_inches='tight', dpi=300)




#
classes = [("no-macsec-1468", "Ethernet\nMTU 1468"), ("orig-1468", "MACsec\nMTU 1468"), ("frag-1468", "Proposal\nMTU 1468"), ("no-macsec-1500", "Ethernet\nMTU 1500"), ("orig-jumbo-1500", "MACsec\nMTU 1500"), ("frag-1500", "Proposal\nMTU 1500"),  ("no-macsec-2936", "Ethernet\nMTU 2936"), ("orig-jumbo-2936", "MACsec\nMTU 2936"),  ("frag-2936", "Proposal\nMTU 2936")]

create(classes)
