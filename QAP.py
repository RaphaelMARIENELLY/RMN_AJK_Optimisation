import random
import math
import time

def init_data(file_name):
    """Extract data from the text file

    Parameters:
        file_name (str): The file name

    Returns:
        data: a list with the matrix size, the weight matrix (int) and the distance matrix (int) of the QAP
    """
    directory = "qapdata/"
    data = [0, [], []]
    n_data = 0  # Index of the current data

    f = open(directory + file_name, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        listed_line = line.split()
        if len(listed_line) == 0:
            n_data += 1
            row = 0
        elif len(listed_line) == 1:
            data[0] = int(listed_line[0])
            for rows in range(data[0]):
                data[1].append([])
                data[2].append([])
        else:
            data[n_data][row] = listed_line
            row += 1
    # Convert the matrix element (str) into integer
    for row in range(data[0]):
        for col in range(data[0]):
            data[1][row][col] = int(data[1][row][col])
            data[2][row][col] = int(data[2][row][col])
    return data


def display_data(n, d, w):
    """Display the matrix size, the weight matrix and the distance matrix

    Parameters:
        n (int): The matrix size
        d (list): The distance matrix
        w (list): The weight matrix
    """
    print(str(n) + "\n")

    for d_row in d:
        print(d_row)
    print("")

    for w_row in w:
        print(w_row)
    print("")


def fitness(n, d, w, sol, i_nbh, nbh=[], f=0):
    """Calculate the fitness of a solution

    Parameters:
        n (int): The matrix size
        d (list): The distance matrix
        w (list): The weight matrix
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        f (int): The calculated fitness of the solution
    """
    if i_nbh in [1, 2] and nbh != []:
        return fitness_plus(n, d, w, sol, nbh, f)
    return fitness_sym(n, d, w, sol)


def fitness_sym(n, d, w, sol):
    """Calculate the fitness of a solution

    Parameters:
        n (int): The matrix size
        d (list): The  symetric distance matrix
        w (list): The weight matrix
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        f (int): The calculated fitness of the solution
    """
    f = 0
    for i_row in range(n):
        for i_col in range(i_row + 1, n):
            delta = d[i_row][i_col] * w[sol[i_row]][sol[i_col]]
            f += delta
    return f*2


def fitness_plus(n, d, w, nbh, sol, f):
    """Calculate the fitness of a solution

    Parameters:
        n (int): The matrix size
        d (list): The  symetric distance matrix
        w (list): The weight matrix
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        f (int): The calculated fitness of the solution
    """
    [emp1, emp2] = get_transposition(n, sol, nbh)
    minus , plus = 0, 0
    for emp in range(n):
        minus += d[emp1][emp] * w[sol[emp1]][sol[emp]]
        plus += d[emp1][emp] * w[nbh[emp1]][nbh[emp]]

        minus += d[emp2][emp] * w[sol[emp2]][sol[emp]]
        plus += d[emp2][emp] * w[nbh[emp2]][nbh[emp]]

    f = f - minus *2
    f = f + plus *2
    return f


def get_transposition(n, sol, nbh):
    r = []
    for idx in range(n):
        if sol[idx] != nbh[idx]:
            r.append(idx)
            if len(r) == 2:
                return r


def random_solution(n):
    """Generate a random solution with a size of n

    Parameters:
        n (int): The size of the solution

    Returns:
        sol (list): A random solution with a size of n
    """
    choix = [equipment for equipment in range(n)]
    sol = []

    for i in range(n):
        e = random.choice(choix)
        sol.append(e)
        choix.remove(e)
    return sol


def neighbourhood(sol, i_nbh, tabou=[]):
    """Generate the neighbourhood of the solution sol with the nbh neighbourhood

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    neighbourhood = []
    if i_nbh == 1:
        return swap_nbhood(sol, tabou)
    if i_nbh == 2:
        return neighbourhood2(sol, tabou)
    if i_nbh == 3:
        return cycle_nbhood(sol, tabou)
    return neighbourhood


def swap_nbhood(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol by swapping 2 equipmments

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    neighbourhood = []
    for i in range(len(sol)):
        for j in range(i):
            if not([i,j] in tabou or [j, i] in tabou):
                neighbourhood.append(sol[::])
                neighbourhood[-1][i], neighbourhood[-1][j] = neighbourhood[-1][j], neighbourhood[-1][i]
    return neighbourhood


def neighbourhood2(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    neighbourhood = []

    for i in range(len(sol)-1):
        if not([i, i+1] in tabou or [i+1, i] in tabou):
            neighbourhood.append(sol[::])
            neighbourhood[-1][i], neighbourhood[-1][i+1] = neighbourhood[-1][i+1], neighbourhood[-1][i]
    if not ([0, len(sol)-1] in tabou or [len(sol)-1, 0] in tabou):
        neighbourhood.append(sol[::])
        neighbourhood[-1][len(sol)-1], neighbourhood[-1][0] = neighbourhood[-1][0], neighbourhood[-1][len(sol)-1]
    return neighbourhood


def cycle_nbhood(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    neighbourhood = []

    for i in range(len(sol)):
        if i not in tabou:
            h = sol[:len(sol)-1+i:]
            t = sol[len(sol)-1+i::]
            neighbour = t + h
            #TODO TABOU
            neighbourhood.append(neighbour)
    return neighbourhood


def random_neighbour(sol, i_nbh):
    """Choose a random element from the neighbourhood of the solution sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    if i_nbh in [1,2]:
        emp1 = random.randint(0,len(sol))
        emp2 = random.randint(0,len(sol))
        while emp1 == emp2:
            emp2 = random.randint(0, len(sol))
        nbh = sol[::]
        nbh[emp1], nbh[emp2] = nbh[emp2], nbh[emp1]
        return nbh

    i = random.randint(0, len(sol))
    h = sol[:len(sol) - 1 + i:]
    t = sol[len(sol) - 1 + i::]
    return t + h


def init_parameters(n, d, w, mu):
    s0 = random_solution(n)
    # Init t0
    max_delta_fitness = 0
    n_positive = 0
    while n_positive < n**2:
        delta_fitness = fitness(n, d, w, random_neighbour(s0)) - fitness(n, d, w, s0)
        if delta_fitness > 0:
            n_positive += 1
            if max_delta_fitness < delta_fitness:
                max_delta_fitness = delta_fitness
    t0 = - max_delta_fitness / math.log(0.8)
    # Init n1
    n1 = int(math.log(-max_delta_fitness / (t0*math.log(0.01))) / math.log(mu))
    # Init n2
    n2 = n1  # TODO
    return [s0, t0, n1, n2]


def simulated_annealing(n, d, w, sol, t, n1, n2, mu):
    print("Parametres : n="+str(n)+" t0="+str(t)+" mu="+str(mu)+" n1="+str(n1)+" n2="+str(n2))
    sol_fitness = fitness(n, d, w, sol)
    best_sol = sol[::]
    best_fitness = fitness(n, d, w, best_sol)
    step = 0
    for i_n1 in range(n1):
        """print("Move n1 = "+str(i_n1))
        print(best_sol)
        print(best_fitness)"""
        for i_n2 in range(n2):
            new_sol = random_neighbour(sol)
            new_fitness = fitness(n, d, w, new_sol)
            delta_fitness = new_fitness - sol_fitness
            if delta_fitness >= 0:
                sol = new_sol[::]
                if new_fitness > best_fitness:
                    best_sol, best_fitness = new_sol[::], new_fitness
            else:
                p = random.random()
                if p <= math.exp(-delta_fitness/t):
                    sol = new_sol[::]
        t *= mu
        #print()
    return [best_sol, best_fitness]


def tabou(n, d, w, sol, size_t, maxIter, nbh):
    """ DOC TODO """
    call_fitness = 0
    sol_fitness, call_fitness = fitness_sym(n, d, w, sol), call_fitness + 1
    tabou = []
    best_solution = sol[::]
    best_fitness, call_fitness = fitness(n, d, w, sol), call_fitness + 1

    best_candidate = sol[::]

    for iter in range(maxIter):
        # Selection
        candidates = neighbourhood(sol, nbh, tabou)

        best_candidate_fitness = math.inf
        for candidate in candidates:
            candidate_fitness, call_fitness = fitness(n, d, w, candidate), call_fitness + 1
            if candidate_fitness < best_candidate_fitness:
                best_candidate_fitness, best_candidate = candidate_fitness, candidate[::]

        # Delta
        delta = best_candidate_fitness - sol_fitness
        if delta > 0:
            if nbh in [1, 2]:
                tabou.append(permutation(sol, best_candidate))
            elif nbh == 3:
                tabou.append(cycle(sol, best_candidate))
            if len(tabou) > size_t:
                tabou = tabou[1::]

        # Update
        sol = best_candidate[::]
        sol_fitness = best_candidate_fitness

        if sol_fitness< best_fitness:
            best_fitness = sol_fitness
            best_solution = sol[::]

        """
        print(sol)
        print(sol_fitness)
        print()
        print(best_solution)
        print(best_fitness)
        print("\n\n")
        """
    return [best_solution, best_fitness, call_fitness]


def permutation(sol1, sol2):
    """Doc TODO"""
    m = []
    for i in range(len(sol1)):
        if sol1[i] != sol2[i]:
            m.append(i)
    return m


def cycle(sol1, sol2):
    for i in range(len(sol1)):
        if sol1[0] == sol2[i]:
            return i