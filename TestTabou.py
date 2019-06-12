from QAP import *
from graphe import *
import time


def test_tabou_size(n, d, w, sol, file, max_iter):
    dir = "data/tai_" +str(n)+"a_"
    donnees = []

    info = "iter:" + str(max_iter) + "    file:"+file +"    start:" + str(sol)
    print(info)
    fichier_i = open(dir+".txt", "a")
    fichier_i.write(info + "\n")
    fichier_i.close()

    for size_t in range(0, 41, 5):
        if size_t % 10 == 0:
            print("T:" + str(size_t))
        t1 = time.time()
        solution1 = tabou(n, d, w, sol, size_t, max_iter, 1)
        t2 = time.time()
        d1 = t2-t1

        info = "V1 T: "+ str(size_t) + "   f:" + str(solution1[1]) + "   nb_f:" + str(solution1[2])+"    time: " + str(d1)
        fichier_i = open(dir+".txt", "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #  -----------------------------------------------

        t1 = time.time()
        solution2 = tabou(n, d, w, sol, size_t, max_iter, 2)
        t2 = time.time()
        d2 = t2 - t1
        info = "V2 T: "+ str(size_t) + "   f:" + str(solution2[1]) + "   nb_f:" + str(solution2[2])+"    time: " + str(d2)

        fichier_i = open(dir+".txt", "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #  -------------------------------------------------------------------------------------------------------

        t1 = time.time()
        solution3 = tabou(n, d, w, sol, size_t, max_iter, 3)
        t2 = time.time()
        d3 = t2 - t1
        info = "V3 T: "+ str(size_t) + "   f:" + str(solution3[1]) + "   nb_f:" + str(solution3[2])+"    time: " + str(d3)

        fichier_i = open(dir+".txt", "a")
        fichier_i.write(info + "\n")
        fichier_i.close()

        #  --------------------------------------------------------------------------------------------------------

        donnees.append((size_t, [solution1[1], solution2[1], solution3[1]]))

    graphiquexls(dir + str(max_iter), donnees)


def test_tabou_iter():

    files = ["tai12a.txt", "tai15a.txt", "tai17a.txt", "tai20a.txt", "tai25a.txt", "tai30a.txt", "tai35a.txt",
             "tai40a.txt", "tai50a.txt", "tai60a.txt", "tai80a.txt", "tai100a.txt"]

    start_sol = [random_solution(size) for size in [12, 15, 17, 20, 25, 30, 35, 40, 50, 60, 80, 100]]
    print("START SOL : " + str(start_sol))

    for maxiter in [100, 1000, 10000]:
        for i_file in range(len(files)):
            data = init_data(files[i_file])
            n = data[0]
            d = data[1]
            w = data[2]

            test_tabou_size(n, d, w, start_sol[i_file], files[i_file], maxiter)


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