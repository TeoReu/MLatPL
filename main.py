import math

from matplotlib import animation, pyplot as plt

from planets import *
from utils import *

Me = 6e10 #6e24
Ms= 2e30
Mj =1.9e27


def lagrange(variables):
    x, y  = variables[0]
    vx, vy = [0, -2.7611061613503196] # these are not used rn

    # To enable 4 parameters: UNCOMMENT THIS and COMMENT ABOVE. Same at line 58 in utils.py
    #x, y, vx, vy = variables[0]


    r, rj, t, KE, PE, AM, AreaVal = f(Me, Ms, Mj, position_X=x, position_Y=y, velocity_X=vx, velocity_Y=vy)
    # loss = 0
    # initial = math.sqrt(r[0][0]**2 + r[0][1]**2)
    # for i,j in r:
    #     if abs(initial - math.sqrt(i**2 + j**2)) > initial:
    #         loss += initial
    #     else:
    #         loss += abs(initial - math.sqrt(i**2 + j**2))
    # print(f"Loss: {loss}")


    loss = 0
    initial = math.sqrt(r[0][0]**2 + r[0][1]**2)

    angle_diff = 0
    unit_vector_1 = r[0] / np.linalg.norm(r[0])
    unit_vector_2 = rj[0] / np.linalg.norm(rj[0])
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    initial_angle = np.arccos(dot_product)
    for v1, v2 in zip(r,rj):
        unit_vector_1 = v1 / np.linalg.norm(v1)
        unit_vector_2 = v2 / np.linalg.norm(v2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        angle_diff += abs(initial_angle - angle)

        i,j = v1
        if abs(initial - math.sqrt(i**2 + j**2)) > initial:
            loss += initial
        else:
            loss += abs(initial - math.sqrt(i**2 + j**2))

    print(f"Loss: {loss}")
    print(f"Angle diff: {angle_diff}")
    print(f"Combined loss: {loss + angle_diff*20}\n")
    return loss + angle_diff*20

#print(lagrange([[-5.17, 0]]))
r, rj, t, KE, PE, AM, AreaVal = f(Me, Ms, Mj, position_X=-5.2, position_Y=0, velocity_X=0, velocity_Y=-2.7611061613503196)


lbl = 'orbit'
py.plot(0,0,'ro',linewidth = 7)
mplot(1,r[:,0],r[:,1],r'$x$ position (AU)',r'$y$ position (AU)','blue','Earth')
mplot(1,rj[:,0],rj[:,1],r'$x$ position (AU)',r'$y$ position (AU)','green','Super Jupiter')
py.ylim([-9, 9])

py.axis('equal')
mplot(2,t,KE,r'Time, $t$ (years)',r'Kinetice Energy, $KE$ ($\times$'+str("%.*e"%(2, EE))+' Joule)','blue','KE')
mplot(2,t,PE,r'Time, $t$ (years)',r'Potential Energy, $KE$ ($\times$'+str("%.*e"%(2, EE))+' Joule)','red','PE')
mplot(2,t,KE+PE,r'Time, $t$ (years)',r'Total Energy, $KE$ ($\times$'+str("%.*e"%(2, EE))+' Joule)','black','Total Energy')
q=py.legend(loc = 0)
q.draw_frame(False)
py.ylim([-180, 180])

mplot(3,t,AM,r'Time, $t$ (years)',r'Angular Momentum','black',lbl)
py.ylim([4, 8])

mplot(4,t,AreaVal,r'Time, $t$ (years)',r'Sweeped Area ($AU^2$)','black',lbl)



fig, ax = py.subplots()
ax.axis('square')
ax.set_xlim(( -7.2, 7.2))
ax.set_ylim((-7.2, 7.2))
ax.get_xaxis().set_ticks([])    # enable this to hide x axis ticks
ax.get_yaxis().set_ticks([])    # enable this to hide y axis ticks

ax.plot(0,0,'o',markersize = 9, markerfacecolor = "#FDB813",markeredgecolor ="#FD7813" )
line1, = ax.plot([], [], 'o-',color = '#d2eeff',markevery=10000, markerfacecolor = '#0077BE',lw=2)   # line for Earth
line2, = ax.plot([], [], 'o-',color = '#e3dccb',markersize = 8, markerfacecolor = '#f66338',lw=2,markevery=10000)   # line for Jupiter

ax.plot([-6,-5],[6.5,6.5],'r-')
ax.text(-4.5,6.3,r'1 AU = $1.496 \times 10^8$ km')

ax.plot(-6,-6.2,'o', color = '#d2eeff', markerfacecolor = '#0077BE')
ax.text(-5.5,-6.4,'Earth')

ax.plot(-3.3,-6.2,'o', color = '#e3dccb',markersize = 8, markerfacecolor = '#f66338')
ax.text(-2.9,-6.4,'Super Jupiter (500x mass)')

ax.plot(5,-6.2,'o', markersize = 9, markerfacecolor = "#FDB813",markeredgecolor ="#FD7813")
ax.text(5.5,-6.4,'Sun')
ttl = ax.text(0.24, 1.05, '', transform = ax.transAxes, va='center')
#plt.title('Elapsed time, T=%i years' %u)


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    ttl.set_text('')

    return (line1, line2, ttl)

def animate(i):
    earth_trail = 40;
    jupiter_trail = 200;
    tm_yr = 'Elapsed time = ' + str(round(t[i], 1)) + ' years'
    ttl.set_text(tm_yr)
    line1.set_data(r[i:max(1, i - earth_trail):-1, 0], r[i:max(1, i - earth_trail):-1, 1])
    line2.set_data(rj[i:max(1, i - jupiter_trail):-1, 0], rj[i:max(1, i - jupiter_trail):-1, 1])
    return (line1, line2)

# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=1000, interval=5, blit=True)
# anim.save('orbit.mp4', fps=30,dpi = 500, extra_args=['-vcodec', 'libx264'])