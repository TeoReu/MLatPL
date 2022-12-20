import GPyOpt


# Example for intialising domain- Continuous domain
# space = [{'name': 'var_1', 'type': 'continuous', 'domain': (-1, 1), 'dimensionality': 1},
#          {'name': 'var_2', 'type': 'continuous', 'domain': (-3, 1), 'dimensionality': 2},
#          {'name': 'var_3', 'type': 'bandit', 'domain': [(-1, 1), (1, 0), (0, 1)], 'dimensionality': 2},
#          {'name': 'var_4', 'type': 'bandit', 'domain': [(-1, 4), (0, 0), (1, 2)]},
#          {'name': 'var_5', 'type': 'discrete', 'domain': (0, 1, 2, 3)}]


def example():
    def myf(x):
        return (2*x)**2
    space = [{'domain': (-1, 1)}]
    max_iter = 15

    myProblem = GPyOpt.methods.BayesianOptimization(f=myf, domain=space)
    myProblem.run_optimization(max_iter)

   # myProblem contains now everything about the BO of the function
   # myProblem.plot_acquisition() to plot the acquisition function


def bo_on_l3_lagrange_point(f, max_iter):
    # L3 is a point that is on the line defined by earth and sun at the other side of the sun
    # take sun at coordinates [0,0] and earth at [1,0], then the third planet would be somewhere around
    # [-a,0] with a positive number.
    # for velocity earth's velocity vector will be orientated down perpendicular on Ox axis
    # for velocity of the third object we know the orientation it up perpendicular on Ox axis
    # what we don't know is the magnitude, the value of the speed


    space = [{'name': 'x_coordinate_of_planet_3', 'type': 'continuous', 'domain': (-10, 10)},
         {'name': 'velocity_magnitude_of_planet_3', 'type': 'continuous', 'domain': (0, 100)}]

    stability = GPyOpt.methods.BayesianOptimization(f=f, domain=space)
    stability.run_optimization(max_iter)

    #in stability.x_opt we have best values for
    return stability




