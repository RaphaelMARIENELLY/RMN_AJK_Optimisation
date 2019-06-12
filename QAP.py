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

    for d_row in d:
        print(d_row)
    print("")

    for w_row in w:
        print(w_row)
    print("")


def random_solution(n):
    """Generate a random solution with a size of n

    Parameters:
        n (int): The size of the solution

    Returns:
        sol (list): A random solution with a size of n
    """
    elements = [e for e in range(n)]
    sol = []
    for i in range(n):
        e = random.choice(elements)
        sol.append(e)
        elements.remove(e)
    return sol


def swap_nbr(sol, move):
    """Generate the neighbour of the solution sol by swapping 2 equipments which are located in move spots

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment
        move (list): The spots to swap

    Returns:
        nbr (list): The neighbour of sol
    """
    nbr = sol[::]
    nbr[move[0]], nbr[move[1]] = nbr[move[1]], nbr[move[0]]
    return nbr


def get_swap(n, sol, nbr):
    """Return the swap between sol and nbr

        Parameters:
            n(int): len of sol
            sol (list): The solution. sol[n_spot] = n_equipment
            nbr (list): A neighbour of sol1

            Returns:
                move (int): The move
            """
    move = []
    for idx in range(n):
        if sol[idx] != nbr[idx]:
            move.append(idx)
            if len(move) == 2:
                return move


def cycle_nbr(sol, move):
    """Generate the neighbour of the solution sol by a circular permutation

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment
        move (int): The index of the move

    Returns:
        nbr (list): The neighbour of sol by move
    """
    h = sol[:move:]
    t = sol[move::]
    m = int(len(t)/2)
    return h + t[m::] + t[:m:]


def get_cycle(n, sol1, nbr):
    """Return the move by a circular permutation between sol and nbr

    Parameters:
        n(int): len of sol
        sol1 (list): The solution. sol[n_spot] = n_equipment
        nbr (list): A neighbour of sol1

        Returns:
            move (int): The move
        """
    for i in range(n):
        if sol1[0] == nbr[i]:
            return i


def random_neighbour(sol, i_nbhood):
    """Choose a random element from the neighbourhood of the solution sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    if i_nbhood in [1, 2]:
        emp1 = random.randint(0,len(sol))
        emp2 = random.randint(0,len(sol))
        while emp1 == emp2:
            emp2 = random.randint(0, len(sol))
        return swap_nbr(sol, [emp1, emp2])

    move = random.randint(1, len(sol))
    return cycle_nbr(sol, move)


def fitness(n, d, w, sol, i_nbhood, nbr=[], f=0):
    """Calculate the fitness of a solution depending on i_nbh

    Parameters:
        n (int): The matrix size
        d (list): The distance matrix
        w (list): The weight matrix
        sol (list): The solution. sol[n_spot] = n_equipment
        i_nbhood (int) : = 1 or 2 -> permutation, =3 -> cycle
        nbr (list): the previous neighbour
        f (int) : the previous neighbour fitness

    Returns:
        f (int): The calculated fitness of the solution
    """
    if i_nbhood in [1, 2] and nbr != []:
        return fitness_plus(n, d, w, sol, nbr, f)
    return fitness_sym(n, d, w, sol)


def fitness_sym(n, d, w, sol):
    """Calculate the fitness of a solution with d symetric

    Parameters:
        n (int): The matrix size
        d (list): The  symmetric distance matrix
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


def fitness_plus(n, d, w, nbr, sol, f):
    """Calculate the fitness of a solution depending on its neighbour fitness

    Parameters:
        n (int): The matrix size
        d (list): The  symmetric distance matrix
        w (list): The weight matrix
        nbr (list): The solution. sol[n_spot] = n_equipment
        sol (list): the previous neighbour
        f (int) : the previous neighbour fitness

    Returns:
        f (int): The calculated fitness of the solution
    """
    [emp1, emp2] = get_swap(n, sol, nbr)
    minus , plus = 0, 0
    for emp in range(n):
        minus += d[emp1][emp] * w[sol[emp1]][sol[emp]]
        plus += d[emp1][emp] * w[nbr[emp1]][nbr[emp]]
        minus += d[emp2][emp] * w[sol[emp2]][sol[emp]]
        plus += d[emp2][emp] * w[nbr[emp2]][nbr[emp]]
    f = f - minus * 2  # Because d is symmetric
    f = f + plus * 2
    return f


def neighbourhood(sol, i_nbhood, tabou=[]):
    """Generate the neighbourhood of the solution sol with the nbh neighbourhood

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment
        i_nbhood (int) : = 1 or 2 -> permutation, =3 -> cycle
        tabou (list): a tabou list with banned moves

    Returns:
        neighbourhood (list): The list of the neighbourhood of sol
    """
    if i_nbhood == 1:
        return swap_nbhood(sol, tabou)
    if i_nbhood == 2:
        return swap_nbhood_bis(sol, tabou)
    if i_nbhood == 3:
        return cycle_nbhood(sol, tabou)
    return []


def swap_nbhood(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol by swapping 2 equipments of sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment
        tabou (list): a tabou list with banned moves

    Returns:
        nbhood (list): The list of the neighbourhood of sol
    """
    nbhood = []
    for i in range(len(sol)):
        for j in range(i):
            if not([i, j] in tabou or [j, i] in tabou):
                nbhood.append(swap_nbr(sol, [i, j]))
    return nbhood


def swap_nbhood_bis(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol by swapping 2 consecutive equipments of sol

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment
        tabou (list): a tabou list with banned moves

    Returns:
        nbhood (list): The list of the neighbourhood of sol
    """
    nbhood = []

    for i in range(len(sol)-1):
        if not([i, i+1] in tabou or [i+1, i] in tabou):
            nbhood.append(swap_nbr(sol, [i, i+1]))
    n = len(sol)
    if not ([0, n-1] in tabou or [n-1, 0] in tabou):
        nbhood.append(swap_nbr(sol, [0, n-1]))
    return nbhood


def cycle_nbhood(sol, tabou=[]):
    """Generate the neighbourhood of the solution sol by a circular permutation

    Parameters:
        sol (list): The solution. sol[n_spot] = n_equipment
        tabou (list): a tabou list with banned moves

    Returns:
        nbhood (list): The list of the neighbourhood of sol
    """
    nbhood = []
    n = len(sol)
    for move in range(1, n):
        if move not in tabou:
            nbhood.append(cycle_nbr(sol, move))
    return nbhood


def init_parameters(n, d, w, mu, p_t0, p_n1):
    s0 = random_solution(n)
    f0 = fitness_sym(n, d, w, s0)
    # Init t0
    max_delta_fitness = 0
    n_positive = 0
    while n_positive < n:
        delta_fitness = fitness(n, d, w, random_neighbour(s0, 1), 1, s0, f0) - f0
        if delta_fitness > 0:
            n_positive += 1
            if max_delta_fitness < delta_fitness:
                max_delta_fitness = delta_fitness
    t0 = - max_delta_fitness / math.log(p_t0)

    # Init n1
    n1 = int(math.log(-max_delta_fitness / (t0*math.log(p_n1))) / math.log(mu))

    # Init n2
    n2 = n1  # TODO
    return [s0, t0, n1, n2]


def simulated_annealing(n, d, w, sol, t, n1, n2, mu, i_nbhood):
    print("Parametres : n="+str(n)+" t0="+str(t)+" mu="+str(mu)+" n1="+str(n1)+" n2="+str(n2))
    sol_fitness = fitness(n, d, w, sol, 1)
    best_sol = sol[::]
    best_fitness = fitness(n, d, w, best_sol, i_nbhood)

    for i_n1 in range(n1):
        for i_n2 in range(n2):
            new_sol = random_neighbour(sol, i_nbhood)
            new_fitness = fitness(n, d, w, new_sol, i_nbhood, sol, sol_fitness)
            delta_fitness = new_fitness - sol_fitness
            if delta_fitness >= 0:
                sol = new_sol[::]
                sol_fitness = new_fitness
                if new_fitness > best_fitness:
                    best_sol, best_fitness = new_sol[::], new_fitness
            else:
                p = random.random()
                if p <= math.exp(-delta_fitness/t):
                    sol = new_sol[::]
                    sol_fitness = new_fitness
        t *= mu
    return [best_sol, best_fitness]


def tabou(n, d, w, sol, size_t, maxIter, i_nbhood):
    """ DOC TODO """
    tabou, call_fitness = [], 0
    sol_fitness, call_fitness = fitness_sym(n, d, w, sol), call_fitness + 1

    best_solution = sol[::]
    best_fitness, call_fitness = fitness(n, d, w, sol, 1), call_fitness + 1

    best_candidate = sol[::]

    for iter in range(maxIter):
        # Selection
        candidates = neighbourhood(sol, i_nbhood, tabou)

        best_candidate_fitness = math.inf
        for candidate in candidates:
            candidate_fitness, call_fitness = fitness(n, d, w, candidate, i_nbhood, sol, sol_fitness), call_fitness + 1
            if candidate_fitness < best_candidate_fitness:
                best_candidate_fitness, best_candidate = candidate_fitness, candidate[::]

        # Delta
        delta = best_candidate_fitness - sol_fitness
        if delta > 0:
            if i_nbhood in [1, 2]:
                tabou.append(get_swap(n, sol, best_candidate))
            elif i_nbhood == 3:
                tabou.append(get_cycle(n, sol, best_candidate))
            if len(tabou) > size_t:
                tabou = tabou[1::]

        # Update
        sol = best_candidate[::]
        sol_fitness = best_candidate_fitness

        if sol_fitness < best_fitness:
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




