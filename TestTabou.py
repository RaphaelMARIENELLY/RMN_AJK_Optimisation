from QAP import *
from graphe import *
import time


def test_tabou_size(n, d, w, sol, file, max_iter):
    dir = "data/"
    donnees = []
    for size_t in range(0, 21, 1):
        t1 = time.time()
        solution1 = tabou(n, d, w, sol, size_t, max_iter, 1)
        t2 = time.time()
        d1 = t2-t1

        info = "maxIter:" + str(max_iter) + " Size : " + str(size_t) + " Solution1 " + str(solution1[0]) + " fitness:" \
               + str(solution1[1]) + " Nb Appel fitness : " + str(solution1[2]) + "    durée: " + str(d1)
        print(info)

        fichier_i = open(dir + "test1_" + file, "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #  -----------------------------------------------

        t1 = time.time()
        solution2 = tabou(n, d, w, sol, size_t, max_iter, 2)
        t2 = time.time()
        d2 = t2 - t1
        info = "maxIter:" + str(max_iter) + " Size : " + str(size_t) + " Solution2 " + str(solution2[0]) + " fitness:" \
               + str(solution2[1]) + " Nb Appel fitness : " + str(solution2[2]) + "    durée: " + str(d2)
        print(info)

        fichier_i = open(dir + "test2_" + file, "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #  -------------------------------------------------------------------------------------------------------

        t1 = time.time()
        solution3 = tabou(n, d, w, sol, size_t, max_iter, 3)
        t2 = time.time()
        d3 = t2 - t1
        info = "maxIter:" + str(max_iter) + " Size : " + str(size_t) + " Solution3 " + str(solution3[0]) + " fitness:"\
               + str(solution3[1]) + " Nb Appel fitness : " + str(solution3[2]) + "    durée: " + str(d3)
        print(info)

        fichier_i = open(dir + "test3_" +file, "a")
        fichier_i.write(info + "\n")
        fichier_i.close()

        #  --------------------------------------------------------------------------------------------------------

        donnees.append((size_t, [solution1[1], solution2[1], solution3[1]]))

    graphiquexls(dir + file + "Iter" + str(max_iter), donnees)


def test_tabou_iter():

    files = ["tai12a.txt", "tai15a.txt", "tai17a.txt", "tai20a.txt", "tai25a.txt", "tai30a.txt", "tai35a.txt",
             "tai40a.txt", "tai50a.txt", "tai60a.txt", "tai80a.txt", "tai100a.txt"]

    for file in files:
        data = init_data(file)
        n = data[0]
        d = data[1]
        w = data[2]
        # display_data(n, d, w)

        sol = random_solution(n)

        print("depart des tests : "+str(sol))
        test_tabou_size(n, d, w, sol, file, 10)
        test_tabou_size(n, d, w, sol, file, 100)
        #test_tabou_size(n, d, w, sol, file, 1000)


def test_fitness():
    files = ["tai12a.txt", "tai15a.txt", "tai17a.txt", "tai20a.txt", "tai25a.txt", "tai30a.txt", "tai35a.txt",
             "tai40a.txt",  "tai50a.txt",  "tai60a.txt", "tai80a.txt", "tai100a.txt"]
    for file in files:
        data = init_data(file)
        n = data[0]
        d = data[1]
        w = data[2]
        sol = random_solution(n)
        fit = fitness_sym(n, d, w, sol)

        nbr = random_neighbour(sol, 1)
        i_test = 1000
        t1 = time.time()
        for i in range(i_test):
            fitness(n, d, w, nbr, 1)
        t2 = time.time()

        for i in range(i_test):
            fitness(n, d, w, nbr, 1, sol, fit)
        t3 = time.time()

        d1 = t2-t1
        d2 = t3-t2

        print("File: "+file+"    durée sym:"+str(d1)+"    durée plus: "+str(d2)+"    rapport: " + str(d1/d2))

# test_fitness()

test_tabou_iter()