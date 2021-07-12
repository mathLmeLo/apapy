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
        return total

    def get_solution_for_worker(self, worker):
        total = 0
        for i, value in enumerate(self.workers[worker][:len(self.workers[worker])-1]):
            edge = self.graph.es.find(_from=value, _to=self.workers[worker][i+1])
            total += edge['cost']
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
        visited[0] = True
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
                    if(visited[edge]):
                        continue
                    elif (vertex_edges[edge]['cost'] < vertex_edges[nearest]['cost']):
                        nearest = vertex_edges[edge].target
                visited[nearest] = True
                worker.append(nearest)
                own_visits += 1
                n_visits += 1
            worker.append(0)

# busca local
    def swap(self):
        gain = 0
        dif = 0
        for worker_i, worker in enumerate(self.workers):
            best_solution = self.get_solution_for_worker(worker_i)
            print('Best Solution: {}'.format(best_solution))
            best_i = None
            best_j = None
            for i, value_i in enumerate(worker[:len(worker)-2], start=1):
                # print(i)
                for j, value_j in enumerate(worker[:len(worker)-2], start=1):
                    rm_1 = self.graph.es.find(_from=worker[i-1], _to=worker[i])
                    rm_2 = self.graph.es.find(_from=worker[i], _to=worker[i+1])
                    rm_3 = self.graph.es.find(_from=worker[j-1], _to=worker[j])
                    rm_4 = self.graph.es.find(_from=worker[j], _to=worker[j+1])
                    add_1 = self.graph.es.find(_from=worker[i-1], _to=worker[j])
                    add_2 = self.graph.es.find(_from=worker[j], _to=worker[i+1])
                    add_3 = self.graph.es.find(_from=worker[j-1], _to=worker[i])
                    add_4 = self.graph.es.find(_from=worker[i], _to=worker[j+1])
                    rm = rm_1['cost'] + rm_2['cost'] + rm_3['cost'] + rm_4['cost']
                    add = add_1['cost'] + add_2['cost'] + add_3['cost'] + add_4['cost']
                    new_solution = (best_solution - rm) + add
                    dif = new_solution - best_solution
                    if dif < gain: # ver se realmente houve um ganho 
                        best_i = i
                        best_j = j
                        gain = dif
                        j =  i + 1
        if (best_i is not None) and (best_j is not None):
              tmp = worker[best_i]
              worker[best_i] = worker[best_j]
              worker[best_j] = tmp


if __name__ == '__main__':
    instance = 'instances/n29p7A.txt'

    # nearest neighbor
    problem = Routes(instance)
    problem.nearest_neighbor()
    problem.print_routes()
    print('Solution = {}'.format(problem.get_solution_value()))
    # swap
    print('Swap')
    problem = Routes(instance)
    problem.nearest_neighbor()
    problem.swap()
    problem.print_routes()
    print('Solution = {}'.format(problem.get_solution_value()))
    problem.write_solution_to_file('cup3.txt')


