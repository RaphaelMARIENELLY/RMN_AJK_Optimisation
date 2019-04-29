L = [ i for i in range(10)]
print(L)

f = open("tai12a.txt",'r')
lignes  = f.readlines()
f.close()
for ligne in lignes:
    li = ligne.split()
    print(li)
