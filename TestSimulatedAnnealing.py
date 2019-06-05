from QAP import *

def test_simulated_annealing():
    data = init_data("tai12a.txt")
    n = data[0]
    d = data[1]
    w = data[2]
    #display_data(n, d, w)

    mu = 0.9
    parameters = init_parameters(n, d, w, mu)
    s0 = parameters[0]
    t0 = parameters[1]
    n1 = parameters[2]
    n2 = parameters[3]

    solution = simulated_annealing(n, d, w, s0, t0, n1, n2, mu)
    print("Simutaled Annealing : Solution "+ str(solution[0]) + " fitness:"+ str(solution[1]))
