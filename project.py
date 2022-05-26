import networkx as nx
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


def cascade_att(G, retweet_prob=0.07):
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
