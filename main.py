from matplotlib import animation, pyplot as plt

from planets import *
from utils import *


r, rj, t, KE, PE, AM, AreaVal = f()


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

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=400, interval=5, blit=True)
plt.show()