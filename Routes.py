from igraph import *
import pandas as pd
import math
import numpy as np


class Routes:
    def __init__(self, filename):
        self.dim, self.p = self.get_dim_p(filename)
        df = pd.read_fwf(filename, sep=" ", skiprows=3, header=None)
        self.graph = Graph.Weighted_Adjacency(df.to_numpy(), 'directed', attr='cost', loops=True)
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

    def describe_edges(self, edge_list):
        for each in edge_list:
            print('Edge {} with cost {}'.format(each.tuple, each['cost']))

    def print_routes(self):
        for idx, worker in enumerate(self.workers):
            print('WORKER #{}: {}'.format(idx, worker))

    def get_solution_value(self):
        total = 0
        for worker in self.workers:
            for i, value in enumerate(worker[:len(worker)-1]):
                edge = self.graph.es.find(_from=value, _to=worker[i+1])
                total += edge['cost']
        print('Solution = {}'.format(total))
        return total

    def write_solution_to_file(self, filename):
        total = 0
        arquivo = open('solutions/'+filename, 'a')
        for worker in self.workers:
            for idx, value in enumerate(worker):
                if idx == (len(worker) - 1):
                    arquivo.write(str(value) + ' ; ')
                else:
                    arquivo.write(str(value) + ', ')
        arquivo.close()


    def nearest_neighbor(self):
        edges_list = self.graph.es()
        visited = [False] * self.dim
        n_visits = 0
        for worker in self.workers:
            n_own_visits = ((self.dim-1)-n_visits) if (n_visits + self.p) > (self.dim-1) else self.p
            own_visits = 0
            worker.append(0)
            for address in worker:
                if own_visits == n_own_visits:
                    break
                vertex_edges = edges_list.select(_from=address)
                nearest = address
                for edge in range(len(vertex_edges)):
                    if (vertex_edges[edge]['cost'] < vertex_edges[nearest]['cost']) and (not visited[edge]) and (vertex_edges[edge].target != 0):
                        nearest = vertex_edges[edge].target
                visited[nearest] = True
                worker.append(nearest)
                own_visits += 1
                n_visits += 1
            worker.append(0)


if __name__ == '__main__':
    instance = 'instances/apa_cup/cup3.txt'

    problem = Routes(instance)
    problem.nearest_neighbor()
    problem.print_routes()
    problem.get_solution_value()
    problem.write_solution_to_file('cup3.txt')


