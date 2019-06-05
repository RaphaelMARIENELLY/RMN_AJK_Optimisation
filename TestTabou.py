from QAP import *
from graphe import *

def test_size(maxIter):
    file = "tai12a.txt"
    data = init_data(file)
    n = data[0]
    d = data[1]
    w = data[2]
    sol = [i for i in range(n)]
    #display_data(n, d, w)

    donnees = []
    for size in range(0, 26, 1):
        solution = tabou(n, d, w, sol, size, maxIter)
        print("Size : " + str(size) + " Solution " + str(solution[0]) + " fitness:" + str(solution[1]))
        donnees.append((size, solution[1]))

    graphiquexls(file + "Iter" + str(maxIter), donnees)

test_size(100)