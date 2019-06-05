import random
import math


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
    for w_row in w:
        print(w_row)
    print("")
    for d_row in d:
        print(d_row)
    print("")


def fitness(n, d, w, sol, display=False):
    """Calculate the fitness of a solution

    Parameters:
        n (int): The matrix size
        d (list): The distance matrix
        w (list): The weight matrix
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        f (int): The calculated fitness of the solution
    """
    f = 0
    for i_row in range(n):
        for i_col in range(n):
            delta = d[i_row][i_col] * w[sol[i_row]][sol[i_col]]
            f += delta
    return f


def random_solution(n, nbh):
    """Generate a random solution with a size of n

    Parameters:
        n (int): The size of the solution

    Returns:
        sol (list): A random solution with a size of n
    """
    sol = [equipment for equipment in range(n)]
    for i in range(n**2):
        sol = random_neighbour(sol, nbh)
    return sol



def neighbourhood(sol, nbh, tabou=[]):
    """Generate the neighbourhood of the solution sol with the nbh neighbourhood

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    neighbourhood = []
    if nbh == 1:
        return neighbourhood1(sol, tabou)
    if nbh == 2:
        return neighbourhood2(sol, tabou)
    return neighbourhood


def neighbourhood1(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol

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
    return neighbourhood


def neighbourhood3(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    neighbourhood = []

    for i in range(len(sol)):
        h = sol[:len(sol)-1+i:]
        t = sol[len(sol)-1+i::]
        neighbour = t + h
        #TODO TABOU
        neighbourhood.append(neighbour)
    return neighbourhood

def random_neighbour(sol, nbh):
    """Choose a random element rom the neighbourhood of the solution sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    return random.choice(neighbourhood(sol, nbh))


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


def tabou(n, d, w, sol, length, maxIter, nbh):
    """ DOC TODO """
    nb_fitness = 0
    sol_fitness, nb_fitness = fitness(n, d, w, sol), nb_fitness + 1
    tabou = []
    best_solution = sol[::]
    best_fitness, nb_fitness = fitness(n, d, w, sol), nb_fitness + 1

    for iter in range(maxIter):
        # Selection
        candidates = neighbourhood(sol, nbh, tabou)
        best_candidate_fitness = math.inf
        for candidate in candidates:
            candidate_fitness, nb_fitness = fitness(n, d, w, candidate), nb_fitness + 1
            if candidate_fitness < best_candidate_fitness:
                best_candidate_fitness, best_candidate = candidate_fitness, candidate[::]

        # Delta
        delta = best_candidate_fitness - sol_fitness
        if delta > 0:
            m = permutation(sol, best_candidate)
            tabou.append(permutation(sol, best_candidate))
            if len(tabou) > length:
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
    return [best_solution, best_fitness, nb_fitness]


def permutation(sol1, sol2):
    """Doc TODO"""
    m = []
    for i in range(len(sol1)):
        if sol1[i] != sol2[i]:
            m.append(i)
    return m
