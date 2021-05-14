import time
from copy import deepcopy


def pick_random(s):
    if s:
        elem = s.pop()
        s.add(elem)
        return elem


def chromo_recursive(lists, pattern, indexes=None, s=None, index=None):
    if indexes is None:
        indexes = []
    if s is None:
        s = set()
    if index is None:
        index = 0

    if s >= pattern:
        return indexes
    if index >= len(lists):
        return False

    s1 = chromo_recursive(lists, pattern, indexes + [index], s | set(lists[index]), index + 1)
    s2 = chromo_recursive(lists, pattern, indexes, s, index + 1)

    if not s1 and not s2:
        return False
    if not s1:
        return s2
    if not s2:
        return s1
    if len(s1) < len(s2):
        return s1
    return s2


def bronker(clique, candidates, excluded, list_of_cliques, neighbours):
    """Bron-Kerbosch algorithm with pivot for finding set of all maximal cliques"""

    if not candidates and not excluded:
        list_of_cliques.append(clique)
        return

    pivot = pick_random(candidates) if pick_random(candidates) is not None else pick_random(excluded)

    for v in list(candidates.difference(neighbours[pivot])):
        new_candidates = candidates.intersection(neighbours[v])
        new_excluded = excluded.intersection(neighbours[v])
        bronker(clique + [v], new_candidates, new_excluded, list_of_cliques, neighbours)
        candidates.remove(v)
        excluded.add(v)


def chromo_finder(starting_graph):
    graph = deepcopy(starting_graph)

    # Making inverted graph
    for v1 in range(len(graph)):
        for v2 in range(len(graph)):
            if v1 != v2:
                if graph[v1][v2] == 0:
                    graph[v1][v2] = 1
                else:
                    graph[v1][v2] = 0

    vertices = [x for x in range(len(graph))]
    n = len(vertices)

    # print(f'Starting with vertices = {vertices}')
    list_of_cliques = []
    neighbours = [[]] * n

    for v in range(len(vertices)):
        pom = []
        for g in range(len(vertices)):
            if graph[v][g] == 1:
                pom.append(vertices[g])
        neighbours[vertices[v]] = pom

    # print(f'neighbours = {neighbours}')

    bronker([], set(vertices), set(), list_of_cliques, neighbours)

    list_of_cliques.sort(key=lambda x: len(x), reverse=True)

    # print(f'list_of_cliques = {list_of_cliques}')

    # Finding chromatic number
    pattern = set([x for x in range(n)])

    # print(f'num of cliques = {len(list_of_cliques)}')
    chromo = len(chromo_recursive(list_of_cliques, pattern))

    print(chromo)

    # # Changing graph
    # # print(*graph, '\n', sep='\n')
    # for v in list_of_cliques[0]:
    #     graph[vertices.index(v)] = -1
    #
    # while -1 in graph:
    #     graph.remove(-1)
    #
    # # print(*graph, '\n', sep='\n')
    #
    # for v in range(len(graph)):
    #     for v2 in list_of_cliques[0]:
    #         graph[v][vertices.index(v2)] = -1
    #     while -1 in graph[v]:
    #         graph[v].remove(-1)
    #
    # # print(*graph, '\n', sep='\n')
    #
    # for v in vertices:
    #     if v in list_of_cliques[0]:
    #         vertices[vertices.index(v)] = -1
    #
    # while -1 in vertices:
    #     vertices.remove(-1)

    # print(vertices)


def main():
    name = input('Unesite ime datoteke:   ')

    with open(name, 'r') as f:
        n = f.readline()
        f.readline()
        matrix = []
        for line in f.readlines():
            matrix.append([int(x) for x in line.split()])

    chromo_finder(matrix)


if __name__ == '__main__':
    main()
