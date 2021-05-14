from copy import deepcopy
import multiprocessing as mp
import time


def f_ranks(tmp):
    v, edges = tmp
    print(f'v = {v}')
    print(f'edges = {edges}')
    return sum([v in e for e in edges])


def func_first_i(tmp):
    index, ranks, v = tmp
    return v if ranks[index] == 0 else None


def induced_graph(graph, del_vertices, vertices):
    print(f'induced vertices = {del_vertices}')
    print(f'vertices = {vertices}')
    for v in del_vertices:
        graph[vertices.index(v)] = -1

    while -1 in graph:
        graph.remove(-1)

    print(f'\n\ngraph without vertices 1', *graph, sep='\n')

    for v in graph:
        for del_v in del_vertices:
            v[vertices.index(del_v)] = -1

        while -1 in v:
            v.remove(-1)

    return graph


def chromo_finder_1(graph):
    miss_list = monte_carlo_mis_parallel(graph)

    k = 0
    pattern = [x for x in range(len(graph))]
    helper = []

    while helper != pattern:
        miss = miss_list.pop(0)
        for v in miss:
            if v not in helper:
                helper.append(v)
        helper.sort()

        for case in range(len(miss_list)):
            for v in range(len(miss_list[case])):
                if miss_list[case][v] in helper:
                    miss_list[case][v] = -1

            while -1 in miss_list[case]:
                miss_list[case].remove(-1)

        miss_list = [list(x) for x in sorted(set(tuple(x) for x in miss_list), key=lambda x: len(x), reverse=True)]
        k += 1

    print(f'k = {k}')


def chromo_finder_2(graph):
    chromo = 0

    if len(graph) == 0:
        return 0
    elif len(graph) == 1:
        return 1

    vertices = [x for x in range(len(graph))]

    while len(graph) != 0:
        print(f'\t\t\t\t Starting for {chromo} color with {vertices}\n\n')
        colored = monte_carlo_mis_parallel(graph, deepcopy(vertices))[0]
        graph = induced_graph(graph, colored, vertices)
        print('GRAPH', *graph, sep='\n')
        for v in colored:
            vertices.remove(v)
        chromo += 1

    print(f'THIS IS THE END, SURE  --->  {chromo}')


# Main stuff
def monte_carlo_mis_parallel(graph1, vertices=None):
    n = len(graph1)
    list_of_miss = []
    flag_2 = False
    if vertices is None:
        flag_2 = True
    else:
        vertices_helper = deepcopy(vertices)

    for vertex in range(n):
        graph = deepcopy(graph1)
        big_i = set()

        if flag_2:
            vertices = [x for x in range(n)]
        else:
            vertices = deepcopy(vertices_helper)

        edges = []
        neighbours = []

        print(f'Solving for vertex ---> {vertices[vertex]}')
        print(f'starting vertices = {vertices}')

        for v in range(n):
            pom = []
            for e in range(n):
                if graph[v][e] == 1:
                    if (vertices[e], vertices[v]) not in edges:
                        edges.append((vertices[v], vertices[e]))
                    pom.append(vertices[e])
            neighbours.append(pom)
        print(f'neighbours = {neighbours}')

        # Solving starting vertex
        big_i.add(vertices[vertex])
        del_vertices = deepcopy(neighbours[vertex])
        del_vertices.append(vertices[vertex])

        print(f'big_i = {big_i}')
        print(f'del_vertices = {del_vertices}')
        print('\nold graph: ', *graph, sep='\n')
        graph = induced_graph(graph, del_vertices, vertices)

        print('\n\ngraph: ', *graph, sep='\n')

        vertices.pop(vertex)

        for v in neighbours[vertex]:
            vertices.remove(v)

        for v in neighbours:
            for nv in range(len(v)):
                if v[nv] not in vertices:
                    v[nv] = -1

            while -1 in v:
                v.remove(-1)

        print(f'verticees = {vertices}\nedges12 = {edges}')
        for v in del_vertices:
            pom = []
            y = 0
            for e in edges:
                if v in e:
                    pom.append(edges.index(e))
            print(f'pom = {pom}')
            for index in pom:
                edges.remove(edges[index - y])
                y += 1
            print(f'edges nakon = {edges}')

        print(f'edges23 = {edges}')

        print(f'\nnew neighbours = {neighbours}')
        print(f'new vertices = {vertices}\n')

        # prime q
        q = n
        while True and q != 2 * n:
            flag = True
            for i in range(2, q // 2 + 1):
                if q % i == 0:
                    flag = False
                    break
            if flag:
                break
            q += 1

            # Main Stuff
        while len(graph) != 0:
            with mp.Pool(processes=mp.cpu_count()) as pool:
                ranks = pool.map(f_ranks, [(x, edges) for x in vertices])  # computing ranks -> d(i)
                print(f'ranks = {ranks} for vertices = {vertices}')

                # computing first big_i
                big_i = big_i.union(set(pool.map(func_first_i, [(vertices.index(x), ranks, x) for x in vertices])))
                big_i.discard(None)
                print(f'big_i = {big_i}')

                for v in big_i:
                    if v in vertices:
                        vertices.remove(v)

                if len(vertices) == 0:
                    break

                print(f'vertices = {vertices}')

                v_max = ranks.index(max(ranks))
                print(f'v_max_index = {v_max} for v = {vertices[v_max]}')

                if ranks[v_max] >= n / 16:
                    big_i.add(vertices[v_max])

                    del_vertices = deepcopy(neighbours[vertices[v_max]])
                    del_vertices.append(vertices[v_max])

                    print(f'del_vertices = {del_vertices}')
                    print('\nold graph: ', *graph, sep='\n')
                    graph = induced_graph(graph, del_vertices, vertices)

                    print('\n\ngraph: ', *graph, sep='\n')
                    v_max_vertex = vertices[v_max]
                    vertices.pop(v_max)

                    print(f'TESTING {neighbours}\t{v_max}\t{neighbours[v_max]}')
                    for v in neighbours[v_max_vertex]:
                        vertices.remove(v)

                    for v in neighbours:
                        for nv in range(len(v)):
                            if v[nv] not in vertices:
                                v[nv] = -1

                        while -1 in v:
                            v.remove(-1)

                    print(f'new neighbours = {neighbours}')
                    print(f'\nnew vertices = {vertices}')

        print(f'THE END ----> {big_i}\n\n')
        list_of_miss.append(big_i)

    print(f'FINAL END ------> {list_of_miss}')

    list_of_miss = sorted(list_of_miss, key=lambda x: len(x), reverse=True)
    list_of_miss = [sorted(x) for x in list_of_miss]
    list_of_miss = [list(x) for x in sorted(set(tuple(x) for x in list_of_miss), key=lambda x: len(x), reverse=True)]

    print(f'list_of_miss = {list_of_miss}')
    return list_of_miss


def main():
    with open('graf2.txt', 'r') as f:
        n = f.readline()
        f.readline()
        matrix = []
        for line in f.readlines():
            matrix.append([int(x) for x in line.split()])

    chromo_finder_2(matrix)


if __name__ == '__main__':
    begin = time.time()
    main()
    end = time.time()
