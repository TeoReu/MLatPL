import GPyOpt

# - Continuous
# domain
# space = [{'name': 'var_1', 'type': 'continuous', 'domain': (-1, 1), 'dimensionality': 1},
#          {'name': 'var_2', 'type': 'continuous', 'domain': (-3, 1), 'dimensionality': 2},
#          {'name': 'var_3', 'type': 'bandit', 'domain': [(-1, 1), (1, 0), (0, 1)], 'dimensionality': 2},
#          {'name': 'var_4', 'type': 'bandit', 'domain': [(-1, 4), (0, 0), (1, 2)]},
#          {'name': 'var_5', 'type': 'discrete', 'domain': (0, 1, 2, 3)}]


def myf(x):
    return (2*x)**2

space = [{'name': 'var_1', 'type': 'continuous', 'domain': (-1, 1), 'dimensionality': 1}]
max_iter = 15

myProblem = GPyOpt.methods.BayesianOptimization(f=myf, domain=space)

x = myProblem.run_optimization(max_iter)

print(x)