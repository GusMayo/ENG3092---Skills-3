import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import style

style.use('seaborn-v0_8-darkgrid')

def rungekutta(func, ts, y_0, time_step = 0.01):
    #create a time domain using the timespan ts:
    start = ts[0]
    end = ts[1]
    evaluation_times = np.arange(start, end, time_step)

    delta_t = time_step #calculate the timestep used in the RK4 method
    yq1 = y_0 #set the values inputted into our motion function to find q1 as equal to the initial values determined in the main code in y_0

    graph_ts = []
    graph_ys = []

    #iterate over the RK4 method for each time instance:
    for t in evaluation_times:
        graph_ts.append(t)
        graph_ys.append(yq1)

        q1 = func(t, yq1) #call our motion function
        #this motion function takes in our list of values, yq1, which contains x1, x1, x1dot and x2dot and returns x1dot, x2dot, x1dotdot and x2dotdot
        #this gives us a vector for q1

        yq2 = [yq1[i] + (delta_t/2) * q1[i] for i in range(len(q1))] #generate the values inputted into our motion function to find q2
        q2 = func(t + (delta_t/2), yq2) #find q2 using out motion function

        yq3 = [yq1[i] + (delta_t/2) * q2[i] for i in range(len(q2))] #generate the values inputted into our motion function to find q3
        q3 = func(t + (delta_t/2), yq3) #find q3 using out motion function

        yq4 = [yq1[i] + delta_t * q3[i] for i in range(len(q3))] #generate the values inputted into our motion function to find q4
        q4 = func(t + delta_t, yq4) #find q4 using out motion function

        yq1 = [yq1[i] + (delta_t/6) * (q1[i] + 2 * q2[i] + 2 * q3[i] + q4[i]) for i in range(len(yq1))] #find the y values inputted into our motion 
        #function to find q1 in our next time step

    return graph_ts, graph_ys


def motion(t, y):
    #unpack the state variables and parameters: (the state variables were stored in the y list of the rungekutta function, the parameters were packed into parameters)
    x1, x2, x1dot, x2dot = y
    m1, m2, c1, c12, c2, k1, k12, k2 = parameters

    #apply equations of motion as given in project brief:
    x1dotdot = (-k1 * x1 - k12 * (x1 - x2) - c1 * x1dot - c12 * (x1dot - x2dot)) / m1

    x2dotdot = (-k2 * x2 - k12 * (x2 - x1) - c2 * x2dot - c12 * (x2dot - x1dot)) / m2

    #return values for x1dot and x2dot and calculated values for x1dotdot and x2dotdot
    return [x1dot, x2dot, x1dotdot, x2dotdot]

#set parameters and initial values:
m1, m2 = 5, 5 #masses

c1, c12, c2 = 1.5, 2.5, 1.1 #damping coefficients
k1, k12, k2 = 10, 15, 20 #spring stiffnesses

initial_x1, initial_x2 = -1, 1 #initial displacements
initial_x1dot, initial_x2dot = 0, 0 #initial velocities
initial_x1dotdot, initial_x2dotdot = 0, 0 #initial accelerations

parameters = m1, m2, c1, c12, c2, k1, k12, k2 #pack all of the parameters into a singlke variable to use in the motion function
intial_conditions = [initial_x1, initial_x2, initial_x1dot, initial_x2dot] #put the initial conditions into an array. this will serve as our y_0
timespan = (0, 20) #set a timespan

ts, ys = rungekutta(motion, timespan, intial_conditions) #call our rungekutta function and assign the results to ts and ys
#this function takes a function to approximate, a timespan to approxiamte the function over, and initial conditions for our system

#set up axes:
fig, ax1 = plt.subplots()
fig, ax2 = plt.subplots()
fig, ax3 = plt.subplots()

#format axes:
axes = [ax1, ax2, ax3]

for ax in axes:
    ax.set_xlabel('Time / s', fontsize = 16)
    ax.spines.left.set_visible(True)
    ax.spines.left.set_color('black')
    ax.spines.left.set_position(('data', 0))
    ax.spines.bottom.set_visible(True)
    ax.spines.bottom.set_color('black')
    ax.spines.bottom.set_position(('data', 27))

ax1.set_title('Displacement - Time curves', fontsize = 16)
ax1.set_ylabel('Displacement / m', fontsize = 16)

ax2.set_title('Velocity - Time Curves', fontsize = 16)
ax2.set_ylabel('Velocity / ms^-1')

ax3.set_title('Acceleration - Time Curves', fontsize = 16)
ax3.set_ylabel('Acceleration / ms^-2', fontsize = 16)

#plot results:
ax1.plot(ts, [y[0] for y in ys], color = 'magenta')
ax1.plot(ts, [y[1] for y in ys], color = 'cyan')

ax2.plot(ts, [y[2] for y in ys], color = 'magenta')
ax2.plot(ts, [y[3] for y in ys], color = 'cyan')

plt.show()