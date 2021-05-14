from copy import deepcopy


def simple_complex_luby_mis(graph1, n):
    graph = deepcopy(graph1)
    vertices = set([x for x in range(n)])
    edges = []

    for v in range(n):
        for e in range(n):
            if graph[v][e] == 1 and (e, v) not in edges:
                edges.append((v, e))

    big_i = []
    probability_values = []



def main():
    with open('graf.txt', 'r') as f:
        n = f.readline()
        f.readline()
        matrix = []
        for line in f.readlines():
            matrix.append([int(x) for x in line.split()])
        simple_complex_luby_mis(matrix, n)


if __name__ == '__main__':
    main()
