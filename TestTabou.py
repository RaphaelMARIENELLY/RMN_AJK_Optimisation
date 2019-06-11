from QAP import *
from graphe import *
import time


def test_tabou_size(file, maxIter):
    data = init_data(file)
    n = data[0]
    d = data[1]
    w = data[2]
    sol = [i for i in range(n)]
    #display_data(n, d, w)

    donnees = []

    for size_t in range(0, 21, 1):
        solution1 = tabou(n, d, w, sol, size_t, maxIter, 1)
        info = "maxIter:"+str(maxIter)+" Size : " + str(size_t) + " Solution1 " + str(solution1[0]) + " fitness:" + str(
            solution1[1]) + " Nb Appel fitness : " + str(solution1[2])
        print(info)

        fichier_i = open("test" + file, "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #-----------------------------------------------

        solution2 = tabou(n, d, w, sol, size_t, maxIter, 2)
        info = "maxIter:"+str(maxIter)+" Size : " + str(size_t) + " Solution2 " + str(solution2[0]) + " fitness:" + str(
            solution2[1]) + " Nb Appel fitness : " + str(solution2[2])
        print(info)

        fichier_i = open("test" + file, "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #--------------------------------------------------------------------------------------------------------------

        solution3 = tabou(n, d, w, sol, size_t, maxIter, 3)
        info = "maxIter:" + str(maxIter) + " Size : " + str(size_t) + " Solution3 " + str(
            solution3[0]) + " fitness:" + str(solution3[1]) + " Nb Appel fitness : " + str(solution3[2])
        print(info)

        fichier_i = open("test" + file, "a")
        fichier_i.write(info + "\n")
        fichier_i.close()

        #--------------------------------------------------------------------------------------------------------------

        donnees.append((size_t, [solution1[1], solution2[1], solution3[1]]))

    graphiquexls(file + "Iter" + str(maxIter), donnees)

"""
files = ["tai12a.txt", "tai15a.txt", "tai17a.txt", "tai20a.txt"]
for file in files:
    test_tabou_size(file, 10)
    test_tabou_size(file, 100)
    test_tabou_size(file, 1000)
    """

data = init_data("tai100a.txt")
n = data[0]
d = data[1]
w = data[2]

sol = random_solution(n)
nbh = random_neighbour(sol, 1)

fit = fitness_sym(n, d, w, sol)
print(fit)
i_test = 1000
t1 = time.time()
for i in range(i_test):
    fitness(n, d, w, nbh, 1)
t2 = time.time()
for i in range(i_test):
    fitness(n, d, w, nbh, 1, sol, fit)
t3 = time.time()

d1 = t2-t1
d2 = t3-t2
print("durée sym "+str(d1))
print("durée plus "+str(d2))
print("rapport " + str(d1/d2))
