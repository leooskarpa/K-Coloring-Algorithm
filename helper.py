def f(l3):
    l3.append(-1)


l = [[0, 1, 2, 3], [1, 2, 3, 0], [4, 7]]
l2 = [0, 1]

s = set(tuple(sorted(x)) for x in l)
print(s)
