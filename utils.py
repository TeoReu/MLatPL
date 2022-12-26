import math
import numpy as np
import pylab as py

def force_es(r, GG, Me, Ms):
    F = np.zeros(2)
    Fmag = GG * Me * Ms / (np.linalg.norm(r) + 1e-20) ** 2
    theta = math.atan(np.abs(r[1]) / (np.abs(r[0]) + 1e-20))
    F[0] = Fmag * np.cos(theta)
    F[1] = Fmag * np.sin(theta)
    if r[0] > 0:
        F[0] = -F[0]
    if r[1] > 0:
        F[1] = -F[1]

    return F


def force_js(r, GG, Mj, Ms):
    F = np.zeros(2)
    Fmag = GG * Mj * Ms / (np.linalg.norm(r) + 1e-20) ** 2
    theta = math.atan(np.abs(r[1]) / (np.abs(r[0]) + 1e-20))
    F[0] = Fmag * np.cos(theta)
    F[1] = Fmag * np.sin(theta)
    if r[0] > 0:
        F[0] = -F[0]
    if r[1] > 0:
        F[1] = -F[1]

    return F


def force_ej(re, rj, GG, Me, Mj):
    r = np.zeros(2)
    F = np.zeros(2)
    r[0] = re[0] - rj[0]
    r[1] = re[1] - rj[1]
    Fmag = GG * Me * Mj / (np.linalg.norm(r) + 1e-20) ** 2
    theta = math.atan(np.abs(r[1]) / (np.abs(r[0]) + 1e-20))
    F[0] = Fmag * np.cos(theta)
    F[1] = Fmag * np.sin(theta)
    if r[0] > 0:
        F[0] = -F[0]
    if r[1] > 0:
        F[1] = -F[1]

    return F


def force(r, planet, ro, vo, GG, Ms, Mj, Me):
    if planet == 'earth':
        return force_es(r, GG, Me, Ms) + force_ej(r, ro, GG, Me, Mj)
    if planet == 'jupiter':
        return force_js(r, GG, Mj, Ms) - force_ej(r, ro, GG, Me, Mj)


def dr_dt(t, r, v, planet, ro, vo):
    return v


def dv_dt(t, r, v, planet, ro, vo, Me, Mj, Ms, GG):
    F = force(r, planet, ro, vo, GG, Ms, Mj, Me)
    if planet == 'earth':
        y = F / Me
    if planet == 'jupiter':
        y = F / Mj
    return y


# Differential equation solvers
# ===================================================================
def EulerSolver(t, r, v, h, Me, Mj, Ms, GG):
    z = np.zeros([2, 2])
    r1 = r + h * dr_dt(t, r, v)
    v1 = v + h * dv_dt(t, r, v, Me, Mj, Ms, GG)
    z = [r1, v1]
    return z


def EulerCromerSolver(t, r, v, h, Me, Mj, Ms, GG):
    z = np.zeros([2, 2])
    r = r + h * dr_dt(t, r, v)
    v = v + h * dv_dt(t, r, v, Me, Mj, Ms, GG)
    z = [r, v]
    return z


def RK4Solver(t, r, v, h, planet, ro, vo, Me, Mj, Ms, GG):
    k11 = dr_dt(t, r, v, planet, ro, vo)
    k21 = dv_dt(t, r, v, planet, ro, vo, Me, Mj, Ms, GG)

    k12 = dr_dt(t + 0.5 * h, r + 0.5 * h * k11, v + 0.5 * h * k21, planet, ro, vo)
    k22 = dv_dt(t + 0.5 * h, r + 0.5 * h * k11, v + 0.5 * h * k21, planet, ro, vo, Me, Mj, Ms, GG)

    k13 = dr_dt(t + 0.5 * h, r + 0.5 * h * k12, v + 0.5 * h * k22, planet, ro, vo)
    k23 = dv_dt(t + 0.5 * h, r + 0.5 * h * k12, v + 0.5 * h * k22, planet, ro, vo, Me, Mj, Ms, GG)

    k14 = dr_dt(t + h, r + h * k13, v + h * k23, planet, ro, vo)
    k24 = dv_dt(t + h, r + h * k13, v + h * k23, planet, ro, vo, Me, Mj, Ms, GG)

    y0 = r + h * (k11 + 2. * k12 + 2. * k13 + k14) / 6.
    y1 = v + h * (k21 + 2. * k22 + 2. * k23 + k24) / 6.

    z = np.zeros([2, 2])
    z = [y0, y1]
    return z


# =====================================================================


def KineticEnergy(v, Me):
    vn = np.linalg.norm(v)
    return 0.5 * Me * vn ** 2


def PotentialEnergy(r, GG, Me, Ms):
    fmag = np.linalg.norm(force_es(r, GG, Me, Ms))
    rmag = np.linalg.norm(r)
    return -fmag * rmag


def AngMomentum(r, v, Me):
    rn = np.linalg.norm(r)
    vn = np.linalg.norm(v)
    r = r / rn
    v = v / vn
    rdotv = r[0] * v[0] + r[1] * v[1]
    if rdotv > 1:
        rdotv = 1
    theta = math.acos(rdotv)
    return Me * rn * vn * np.sin(theta)


def AreaCalc(r1, r2):
    r1n = np.linalg.norm(r1)
    r2n = np.linalg.norm(r2)
    r1 = r1 + 1e-20
    r2 = r2 + 1e-20
    theta1 = math.atan(abs(r1[1] / r1[0]))
    theta2 = math.atan(abs(r2[1] / r2[0]))
    rn = 0.5 * (r1n + r2n)
    del_theta = np.abs(theta1 - theta2)
    return 0.5 * del_theta * rn ** 2


def mplot(fign, x, y, xl, yl, clr, lbl):
    py.figure(fign)
    py.xlabel(xl)
    py.ylabel(yl)
    return py.plot(x, y, clr, linewidth=1.0, label=lbl)

