from igraph import *
import pandas as pd
import math
import numpy as np


class Routes:
    def __init__(self, filename):
        self.dim, self.p = self.get_dim_p(filename)
        df = pd.read_fwf(filename, sep=" ", skiprows=3, header=None)
        self.graph = Graph.Weighted_Adjacency(df.to_numpy(), 'undirected', attr='cost', loops=False)
        n_workers = math.ceil((self.dim-1)/self.p)
        self.workers = [[] for _ in range(n_workers)]

    @staticmethod
    def get_dim_p(filename):
        arq = open(filename, 'r')
        lines = arq.readlines()
        arq.close()
        d_ = int(lines[0].split(' ')[1])
        p_ = int(lines[1].split(' ')[1])
        return d_, p_

    def plot_graph(self):
        lyt = self.graph.layout("kk")
        plot(self.graph, layout=lyt)

    def describe_edges(self):
        edges = self.graph.es()
        for each in edges:
            print('Edge {} with cost {}'.format(each.tuple, each['cost']))

    def nearest_neighbor(self):
        vertex_list = self.graph.vs() # todas os vertices do grafo
        edges_list = self.graph.es() # todos as arestas do grafo
        visited = [False] * self.dim # lista auxiliar para manter endereços ja adicionados a solução
        n_visits = 0 # auxiliar para manter numero total de vertices na solução(todos os workers)
        for worker in self.workers: # loop para cada um dos workers na solução
            n_own_visits = ((self.dim-1)-n_visits) if (n_visits + self.p) > (self.dim-1) else self.p # numero de visitas que o worker deve realizar
            own_visits = 0 # quantas visitas já realizou
            worker.append(0) # iniciar rota da base(vertice 0)
            for address in worker: # loop para cada endereço na rota do worker
                if own_visits > n_own_visits: # worker visita ate n_own_visits endereços
                    break
                vertex_edges = edges_list.select(_source=address) # acessar a lista de arestas para o endereço(vertice) atual
                l_cost = 10000 # custo alto para sempre encontrar o mais barato na lista
                nearest = 0 # vertice com aresta de melhor custo
                for edge in range(len(vertex_edges)): # loop para cada aresta na lista de adj do vertice
                    if (vertex_edges[edge]['cost'] < l_cost) and (not visited[edge]):
                        l_cost = vertex_edges[edge]['cost'] # troca o menor custo
                        nearest = vertex_edges[edge].target # indice do vertice com o menor custo de conexao(aresta)
                visited[nearest] = True # setar o vertice como visitado
                worker.append(nearest) # adicionar a solução
                own_visits += 1
                n_visits += 1
        print(self.workers)


if __name__ == '__main__':
    instance = 'instances/n10p4.txt'

    problem = Routes(instance)
    problem.nearest_neighbor()

    # describe_edges(g)
    # plot_graph(g)