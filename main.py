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
    edges = graph.es()
    for each in edges:
        print('Edge {} with cost {}'.format(each.tuple, each['cost']))


def nearest_neighbor(graph):
    vertex_list = graph.vs()
    edges_list = graph.es()
    solution = []
    for vertex in vertex_list:
        vertex_edges = edges_list.select(_source=vertex.index)
        nearer = edges_list[0]['cost']
        s = vertex_edges.select(cost_lt=nearer)
        if len(s) > 0:
            print(min(s['cost']))
        # print("Vertex {} edges are".format(vertex.index))
        # for each in vertex_edges:
        #     print('Edge {} with cost {}'.format(each.tuple, each['cost']))



if __name__ == '__main__':
    instance = 'instances/n10p4.txt'
    dim, p = get_dim_p(instance)
    df = pd.read_fwf(instance, sep=" ", skiprows=3, header=None)

    g = Graph.Weighted_Adjacency(df.to_numpy(), 'undirected', attr='cost', loops=False)

    nearest_neighbor(g)

    # describe_edges(g)
    # plot_graph(g)