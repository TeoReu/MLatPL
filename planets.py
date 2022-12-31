import math
import numpy as np
import pylab as py

from utils import KineticEnergy, PotentialEnergy, AngMomentum, RK4Solver, AreaCalc

G = 6.673e-11  # Gravitational Constant

RR = 1.496e11  # Normalizing distance in km (= 1 AU)
MM = 6e24  # Normalizing mass
TT = 365 * 24 * 60 * 60.0  # Normalizing time (1 year)

FF = (G * MM ** 2) / RR ** 2  # Unit force
EE = FF * RR  # Unit energy

GG = (MM * G * TT ** 2) / (RR ** 3)

ti = 0  # initial time = 0

def f(Me = 6e24, Ms=2e30, Mj=1.9e27, tf = 15, position_X = -5.2, position_Y=0, velocity_X=0, velocity_Y=0):
    # Mass of Earth in kg = Me
    # Mass of Sun in kg = Ms
    # Mass of Jupiter = Mj
    # final time = 120 years = tf
    Me = Me / MM  # Normalized mass of Earth
    Ms = Ms / MM  # Normalized mass of Sun
    Mj = Mj / MM  # Normalized mass of Jupiter/Super Jupiter

    N = 100 * tf  # 100 points per year
    t = np.linspace(ti, tf, N)  # time array from ti to tf with N points

    h = t[2] - t[1]  # time step (uniform)

    # Initialization

    KE = np.zeros(N)  # Kinetic energy
    PE = np.zeros(N)  # Potential energy
    AM = np.zeros(N)  # Angular momentum
    AreaVal = np.zeros(N)

    r = np.zeros([N, 2])  # position vector of Earth
    v = np.zeros([N, 2])  # velocity vector of Earth
    rj = np.zeros([N, 2])  # position vector of Jupiter
    vj = np.zeros([N, 2])  # velocity vector of Jupiter

    ri = [position_X, position_Y]  # initial position of earth
    rji = [5.2, 0]  # initial position of Jupiter

    vv = np.sqrt(Ms * GG / abs(ri[0]))  # Magnitude of Earth's initial velocity
    #print(vv)

    vvj = 13.06e3 * TT / RR  # Magnitude of Jupiter's initial velocity

    angle = math.atan2(position_Y, position_X)

    cos = math.cos(angle)
    sin = math.sin(angle)

    vi = [sin * vv, cos * vv]  # Initial velocity vector for Earth.Taken to be along y direction as ri is on x axis.

    # UNCOMMENT THIS FOR SPEED PARAMETERS
    #vi = [velocity_X, velocity_Y]
    vji = [0, vvj * 1.0]  # Initial velocity vector for Jupiter

    # Initializing the arrays with initial values.
    t[0] = ti
    r[0, :] = ri
    v[0, :] = vi
    rj[0, :] = rji
    vj[0, :] = vji

    """
    t1 = dr_dt(ti,ri,vi)
    t2 = dv_dt(ti,ri,vi)
    print t1
    print t2
    """
    KE[0] = KineticEnergy(v[0, :], Me)
    PE[0] = PotentialEnergy(r[0, :], GG, Me, Ms)
    AM[0] = AngMomentum(r[0, :], v[0, :], Me)
    AreaVal[0] = 0

    for i in range(0, N - 1):
        [r[i + 1, :], v[i + 1, :]] = RK4Solver(t[i], r[i, :], v[i, :], h, 'earth', rj[i, :], vj[i, :], Me, Mj, Ms, GG)
        [rj[i + 1, :], vj[i + 1, :]] = RK4Solver(t[i], rj[i, :], vj[i, :], h, 'jupiter', r[i, :], v[i, :], Me, Mj, Ms, GG)

        KE[i + 1] = KineticEnergy(v[i + 1, :], Me)
        PE[i + 1] = PotentialEnergy(r[i + 1, :], GG, Me, Ms)
        AM[i + 1] = AngMomentum(r[i + 1, :], v[i + 1, :], Me)
        AreaVal[i + 1] = AreaVal[i] + AreaCalc(r[i, :], r[i + 1, :])

    return r, rj, t, KE, PE, AM, AreaVal

        #TODO : check if the positions for each and jupiter are out of the grid
        #return the number of iterations it took


#TODO: write functions that characterise the quality of the initial settings:
# a) how many iterations it takes for the planets to jump of
# b) if the planets jump of their initial trajectories