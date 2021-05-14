import math
import random
import multiprocessing as mp
from copy import deepcopy


####################################################

def f_ranks(tmp):
    v, edges = tmp
    return sum([v in e for e in edges])


def f_coins(r):
    if r == 0:
        return 1
    else:
        return 1 if random.random() <= (1 / (2 * r)) else 0


def f_ending(tmp):
    e, big_x, ranks = tmp

    if e[0] in big_x and e[1] in big_x:
        if ranks[e[0]] <= ranks[e[1]]:
            return e[0]
        else:
            return e[1]

####################################################


def f_new_graph(big_y, vertices, edges):
    new_vertices = set(vertices - big_y)
    new_edges = [e for e in edges if e[0] not in big_y and e[1] not in big_y]

    return new_vertices, new_edges


def func_n(new_big_i, edges):
    neighbours = set()
    for v in new_big_i:
        for e in edges:
            if v in e:
                neighbours.add(e[0 if e[0] != v else 1])
    return neighbours


# Main Function for searching MSI

def monte_carlo_mis(graph1):
    big_i = set()

    n = len(graph1[0])
    graph = deepcopy(graph1)
    vertices = set(x for x in range(n))
    edges = []

    for v in range(n):
        for e in range(n):
            if graph[v][e] == 1 and (e, v) not in edges:
                edges.append((v, e))

    while len(vertices) != 0:
        print(f"Starting with v: {vertices} and e: {edges}")
        with mp.Pool(processes=mp.cpu_count()) as pool:
            ranks = pool.map(f_ranks, [(x, edges) for x in vertices])
            coins = pool.map(f_coins, ranks)
            big_x = [v for v in vertices if coins[v] == 1]

            helper = set(pool.map(f_ending, [(e, big_x, ranks) for e in edges]))
            new_big_i = vertices - helper

        big_i = big_i.union(new_big_i)
        big_y = new_big_i.union(func_n(new_big_i, edges))
        print(f'\nvertices = {vertices}\nedges = {edges}\nnew_big_i = {new_big_i}')
        vertices, edges = f_new_graph(big_y, vertices, edges)

        print(f'\nranks = {ranks}\ncoins = {coins}\nbig_x = {big_x}\nhelper = {helper}\nbig_i = {big_i}\nbig_y = {big_y}\n')
        print(f'vertices = {vertices}\nedges = {edges}')

    return big_i


def main():
    with open('graf.txt', 'r') as f:
        n = f.readline()
        f.readline()
        matrix = []
        for line in f.readlines():
            matrix.append([int(x) for x in line.split()])
        monte_carlo_mis(matrix)


if __name__ == '__main__':
    main()
