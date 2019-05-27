"""L = [ i for i in range(10)]
print(L)

f = open("tai10a.txt",'r')
lignes  = f.readlines()
f.close()
for ligne in lignes:
    li = ligne.split()
    print(li)
"""
L = [[2,3],[5,4]]
if [3,2]  in L or [2, 3]in L:
    print("yes")
