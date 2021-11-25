import numpy as np
import matplotlib.pyplot as plt
import textwrap

#reading txt files (ADC)
data_before = np.genfromtxt("data_before.txt",comments="\n")
data_after = np.genfromtxt("data_after.txt",comments="\n")
P_40 = np.average(np.genfromtxt("P40.txt",comments="\n"))
P_80 = np.average(np.genfromtxt("P80.txt",comments="\n"))
P_120 = np.average(np.genfromtxt("P120.txt",comments="\n"))
P_160 = np.average(np.genfromtxt("P160.txt",comments="\n"))


# finding calibration factor
fig = plt.figure()
ax = fig.add_subplot(111)

location = ['center', 'left', 'right']
myTitle = "Calibration factor"
ax.set_title("\n".join(textwrap.wrap(myTitle, 80)), loc =location[0])
ax.set_ylabel('Pressure, mmHg')
ax.set_xlabel('m*Pressure + c, 1un.')

plt.scatter([P_40, P_80, P_120, P_160], [40, 80, 120, 160], color = 'darkblue')
m, c = np.linalg.lstsq([[P_40, 1], [P_80, 1],  [P_120, 1], [P_160, 1]], [40, 80, 120, 160] , rcond=None)[0]
plt.plot([P_40, P_80, P_120, P_160], m*np.array([P_40, P_80, P_120, P_160]) + c, 'r', label = "lsqm")

plt.legend()

# add a grid
plt.minorticks_on()
plt.grid(which='major', color='lightgrey', linestyle='-', linewidth=1)
plt.grid(which='minor', color='lightgrey', linestyle='--', linewidth=0.5)

# add a text
plt.text(600, 140,"m = {: .2f}".format(m))
plt.text(600, 130,"c = {: .2f}".format(c))


plt.savefig('factor.png')
plt.show()

# plotting data: (linestyle, linewidth, color)
# init times

t = 60
times_1 = np.linspace(0, t, len(data_before))
times_2 = np.linspace(0, t, len(data_after))

r1 = []
r2 = []
for i in range(len(times_2)):
        if(m * data_after[i] + c > 25 and m * data_after[i] + c < 145 and times_2[i]>5):
                r1.append(np.array([times_1[i], m * data_before[i] + c]))
                r2.append(np.array([times_2[i], m * data_after[i] + c]))
res1 = np.array(r1)
res2 = np.array(r2)

# init figure
fig1 = plt.figure()
ax = fig1.add_subplot(111)

z1 = np.polyfit(res1[:, 0], res1[:, 1], 50)
polynom1 = np.poly1d(z1)
x1 = np.linspace(res1[:, 0][0], res1[:, 0][-1], len(res1))

z2 = np.polyfit(res2[:, 0], res2[:, 1], 50)
polynom2 = np.poly1d(z2)
x2 = np.linspace(res2[:, 0][0], res2[:, 0][-1], len(res2))


# init axes
ax.set_xlim([min(res2[:, 0]), 1.0*max(res2[:, 0])])
ax.set_ylim([0, 1.1*max(res2[:, 1])])

myTitle = "Arterial Press plotted"
ax.set_title("\n".join(textwrap.wrap(myTitle, 80)), loc =location[0])
ax.set_ylabel('Pressure, mmHg')
ax.set_xlabel('time, s')

plt.plot( res1[:, 0], res1[:, 1] ,
        linestyle = '-',
        linewidth = 1,
        color = 'darkblue',
        marker='',
        markevery = 50,
        label = 'data before')

plt.plot(res2[:, 0], res2[:, 1],
        linestyle = '-',
        linewidth = 1,
        color = 'darkred',
        marker='',
        markevery = 50,
        label = 'data after')

plt.legend()

# add a grid
plt.minorticks_on()
plt.grid(which='major', color='lightgrey', linestyle='-', linewidth=1)
plt.grid(which='minor', color='lightgrey', linestyle='--', linewidth=0.5)

# add a text


# save plot
plt.savefig('Arterial_press.png')
plt.show()


fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

myTitle = "Pulse"
ax2.set_title("\n".join(textwrap.wrap(myTitle, 80)), loc =location[0])
ax2.set_ylabel('Pressure, mmHg')
ax2.set_xlabel('time, t')

ax2.set_xlim([min(res2[:, 0]), 1.0*max(res2[:, 0])])
ax2.set_ylim([1.1*min(res2[:, 1] - polynom2(x2)), 1.1*max(res2[:, 1] - polynom2(x2))])

plt.plot(res2[:, 0], res2[:, 1]-polynom2(x2),
        linestyle = '-',
        linewidth = 1,
        color = 'darkred',
        marker='',
        markevery = 50,
        label = 'data after')

plt.plot(res1[:, 0], res1[:, 1]-polynom1(x1),
        linestyle = '-',
        linewidth = 1,
        color = 'darkblue',
        marker='',
        markevery = 50,
        label = 'data before')

plt.legend()

# add a grid
plt.minorticks_on()
plt.grid(which='major', color='lightgrey', linestyle='-', linewidth=1)
plt.grid(which='minor', color='lightgrey', linestyle='--', linewidth=0.5)

plt.savefig('pulse.png')
plt.show()