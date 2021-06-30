from igraph import *
import pandas as pd


def get_dim_p(filename):
    arq = open(filename, 'r')
    lines = arq.readlines()
    arq.close()
    d_ = int(lines[0].split(' ')[1])
    p_ = int(lines[1].split(' ')[1])
    return d_, p_


def plot_graph(graph):
    lyt = graph.layout("kk")
    plot(graph, layout=lyt)


def describe_edges(graph):
    edges = g.es()
    for each in edges:
        print('Edge {} with cost {}'.format(each.tuple, each['cost']))


if __name__ == '__main__':
    instance = 'instances/n10p4.txt'
    dim, p = get_dim_p(instance)
    df = pd.read_fwf(instance, sep=" ", skiprows=3, header=None)

    g = Graph.Weighted_Adjacency(df.to_numpy(), 'undirected', attr='cost', loops=False)

    # describe_edges(g)
    # plot_graph(g)