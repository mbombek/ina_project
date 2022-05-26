from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from random import choice, random
from tabulate import tabulate


def twitter():
    G = nx.DiGraph()
    with open("twitter.txt", "r") as lines:
        for line in lines:
            a, b = line.split()
            G.add_edge(int(a), int(b))
    return G


def cascade(G, retweet_prob=0.07, candidates=[], table=True):
    start = choice(list(G.nodes()))

    S = list()
    S.append(start)
    visited = set()

    while S:
        curr = S.pop()

        if curr in visited or curr in candidates:
            continue

        visited.add(curr)
        neighbors = list(G.predecessors(curr))
        for neighbor in neighbors:
            if random() < retweet_prob:
                S.append(neighbor)

    N = G.number_of_nodes()
    V = len(visited)
    if table:
        print(
            tabulate(
                [
                    ["RETWEET PROBABILITY", retweet_prob],
                    ["N", N],
                    ["V", V],
                    ["CASCADE SIZE (V / N)", round(V / N, 2)],
                ],
                tablefmt="fancy_grid",
                numalign="left",
            )
        )
    else:
        return str(round(V / N, 2))


def cascade_att(G, retweet_prob=0.07, debug=False):
    start = choice(list(G.nodes()))

    S = list()
    S.append(start)
    visited = set()

    N = G.number_of_nodes()
    V = 0

    while S:
        curr = S.pop()

        if curr in visited:
            continue

        G.nodes[curr]["cascaded"] += 1
        visited.add(curr)
        neighbors = list(G.predecessors(curr))
        V += 1
        for neighbor in neighbors:
            if random() < retweet_prob:
                S.append(neighbor)

    global_cascade = False if (V / N) < 0.05 else True

    if debug:
        print(
            tabulate(
                [
                    ["RETWEET PROBABILITY", retweet_prob],
                    ["N", N],
                    ["V", V],
                    ["CASCADE SIZE (V / N)", round(V / N, 2)],
                    ["LOCAL OR GLOBAL", "Global" if global_cascade else "Local"],
                ],
                tablefmt="fancy_grid",
                numalign="left",
            )
        )
    return global_cascade

def cascade_agg(G, retweet_prob, candidates):
    start = choice(list(G.nodes()))

    S = list()
    S.append(start)
    visited = set()

    N = G.number_of_nodes()
    V = 0

    while S:
        curr = S.pop()

        if curr in visited or curr in candidates:
            continue

        G.nodes[curr]["cascaded"] += 1
        visited.add(curr)
        neighbors = list(G.predecessors(curr))
        V += 1
        for neighbor in neighbors:
            if random() < retweet_prob:
                S.append(neighbor)

    global_cascade = False if (V / N) < 0.05 else True
    return global_cascade, round((V / N), 2)

def simulate(G, N, retweet_prob, candidates, name=""):
    hist_pre = defaultdict(int)
    hist_post = defaultdict(int)

    prev_prog = 0
    print(f"{name} PRE PROGRESS: [", end="")
    for i in range(N):
        hist_pre[cascade(G, retweet_prob, [], False)] += 1
        
        prog = int((i / N) * 100)
        if prog % 10 == 0 and prog > prev_prog:
            print("#", end="")
            prev_prog = prog
    print("]")

    prev_prog = 0
    print(f"{name} POST PROGRESS: [", end="")
    for i in range(N):
        hist_post[cascade(G, retweet_prob, candidates, False)] += 1
        
        prog = int((i / N) * 100)
        if prog % 10 == 0 and prog > prev_prog:
            print("#", end="")
            prev_prog = prog
    print("]")

    pre_vals = []
    pre_keys = []
    for key in sorted(hist_pre):
        pre_vals.append(hist_pre[key])
        pre_keys.append(key)

    post_vals = []
    post_keys = []
    for key in sorted(hist_post):
        post_vals.append(hist_post[key])
        post_keys.append(key)
    
    plt.figure()
    plt.bar(range(len(pre_vals)), pre_vals, align="center", label="Pre")
    plt.xticks(range(len(pre_keys)), pre_keys)

    plt.bar(range(len(post_vals)), post_vals, align="center", alpha=0.5, label="Post")
    plt.xticks(range(len(post_keys)), post_keys)
    plt.legend()


def simulate_agg(G, N, retweet_prob, candidates):
    l = 0
    g = 0
    g_sum = 0

    for i in range(N):
        c, c_size = cascade_agg(G, retweet_prob, candidates)
        if c:
            g += 1
            g_sum += c_size
        else:
            l += 1
    if g == 0:
        g = 1
    return l, round(g_sum / g, 2)
