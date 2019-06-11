from QAP import *
from graphe import *

def test_tabou_size(file, maxIter):

    data = init_data(file)
    n = data[0]
    d = data[1]
    w = data[2]
    sol = [i for i in range(n)]
    #display_data(n, d, w)

    donnees = []

    for size in range(0, 21, 1):
        solution1 = tabou(n, d, w, sol, size, maxIter, 1)
        info = "maxIter:"+str(maxIter)+" Size : " + str(size) + " Solution1 " + str(solution1[0]) + " fitness:" + str(
            solution1[1]) + " Nb Appel fitness : " + str(solution1[2])
        print(info)

        fichier_i = open("test" + file, "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #-----------------------------------------------

        solution2 = tabou(n, d, w, sol, size, maxIter, 2)
        info = "maxIter:"+str(maxIter)+" Size : " + str(size) + " Solution2 " + str(solution2[0]) + " fitness:" + str(
            solution2[1]) + " Nb Appel fitness : " + str(solution2[2])
        print(info)

        fichier_i = open("test" + file, "a")
        fichier_i.write(info+"\n")
        fichier_i.close()

        #--------------------------------------------------------------------------------------------------------------

        solution3 = tabou(n, d, w, sol, size, maxIter, 3)
        info = "maxIter:" + str(maxIter) + " Size : " + str(size) + " Solution3 " + str(
            solution3[0]) + " fitness:" + str(solution3[1]) + " Nb Appel fitness : " + str(solution3[2])
        print(info)

        fichier_i = open("test" + file, "a")
        fichier_i.write(info + "\n")
        fichier_i.close()

        #--------------------------------------------------------------------------------------------------------------

        donnees.append((size, [solution1[1], solution2[1], solution3[1]]))

    graphiquexls(file + "Iter" + str(maxIter), donnees)


files = ["tai12a.txt", "tai15a.txt", "tai17a.txt", "tai20a.txt"]
for file in files:
    test_tabou_size(file, 10)
    test_tabou_size(file, 100)
    test_tabou_size(file, 1000)
