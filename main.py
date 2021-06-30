from igraph import *
import pandas as pd


def get_dim_p(filename):
    arq = open(filename, 'r')
    lines = arq.readlines()
    arq.close()
    dim = int(lines[0].split(' ')[1])
    p = int(lines[1].split(' ')[1])
    return dim, p


if __name__ == '__main__':
    instance = 'instances/n10p4.txt'
    dim, p = get_dim_p(instance)
    df = pd.read_fwf(instance, sep=" ", skiprows=3, header=None)

    g = Graph.Weighted_Adjacency(df.to_numpy(), 'undirected', attr='cost', loops=False)
    print(g)

    layout = g.layout("kk")
    plot(g, layout=layout)