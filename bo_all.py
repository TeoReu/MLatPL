import GPyOpt
from matplotlib import pyplot as plt
import numpy as np

from main import lagrange

space = [{'name': 'x', 'type': 'continuous', 'domain': (-6, 6)},
         {'name': 'y', 'type': 'continuous', 'domain': (-6, 6)}]
         #{'name': 'vx', 'type': 'continuous', 'domain': (-5, 5)}]
         #{'name': 'vy', 'type': 'continuous', 'domain': (-5, 5)}]

stability = GPyOpt.methods.BayesianOptimization(f=lagrange, domain=space)
stability.run_optimization(500)

# in stability.x_opt we have best values for
print(stability.x_opt)
print(stability.fx_opt)
stability.plot_acquisition()
print(stability.get_evaluations())


#coords, z = stability.get_evaluations()


# x = np.array([coords[:,0].flatten()])
# y = np.array([coords[:,1].flatten()])
# z = np.array([z.flatten()])
#
# print(x)
# print(y)
#
# fig, ax = plt.subplots()
# ax.set_title('Heatmap with Colormesh')
#
# plt.pcolormesh(x, y, z, cmap='RdBu', vmin=-np.abs(z).max(),
#                vmax=np.abs(z).max())
# plt.colorbar()
# plt.show()


