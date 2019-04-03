import matplotlib.pyplot as plt
from scipy.interpolate import splev, splrep
import numpy as np
from scipy import interpolate
import matplotlib.patches as mpatches

data=[]
knots=[]
knots_uniform=[]
control_point_list=[]
control_point_list_uniform=[]
with open("example2.txt", "rt") as file:
    for line in file:
        data.append(list(map(int, line.strip().split(" "))))
with open("example2_output.txt", "rt") as output:
    for idx,line in enumerate(output.readlines()):
        line = line.strip('\n')
        if idx==0:
            k=int(line.strip('\n'))
        elif idx==1:
            num_cpoints=int(line.strip('\n'))
        elif idx==3:
            knot=line.strip('\n').split(' ')
            knot.pop()
            knot=list(map(float,knot))
        elif idx>=5:
            control_point=line.strip("\n").split(' ')
            control_point=list(map(float,control_point))
            control_point_list.append(control_point)

control_point_list=np.array(control_point_list)
control_point_x=control_point_list[:,0]
control_point_y=control_point_list[:,1]

with open("example2_output_uniform.txt", "rt") as output_uniform:
    for idx,line in enumerate(output_uniform.readlines()):
        line = line.strip('\n')
        if idx==0:
            k=int(line.strip('\n'))
        elif idx==1:
            num_cpoints=int(line.strip('\n'))
        elif idx==3:
            knots_uniform=line.strip('\n').split(' ')
            knots_uniform.pop()
            knots_uniform=list(map(float,knots_uniform))
        elif idx>=5:
            control_point_uniform=line.strip("\n").split(' ')
            control_point_uniform=list(map(float,control_point_uniform))
            control_point_list_uniform.append(control_point_uniform)

control_point_list_uniform=np.array(control_point_list_uniform)
control_point_x_uniform=control_point_list_uniform[:,0]
control_point_y_uniform=control_point_list_uniform[:,1]

data=np.array(data)
x=data[:,0]
y=data[:,1]
tck,u = interpolate.splprep([x,y],s=0,k=3)
unew = np.arange(0, 1, 0.01)
u=np.linspace(0,1,num=100,endpoint=True)
out = interpolate.splev(u,tck)

inter_x,inter_y = np.array(interpolate.splev(unew, (knot,control_point_list.T,3)))
inter_x_uniform,inter_y_uniform = np.array(interpolate.splev(unew, (knots_uniform,control_point_list_uniform.T,3)))
plt.figure(figsize=(7,5))
# plt.annotate('End point', xy=(control_point_x[0]+0.25, control_point_y[0]+0.25), xytext=(control_point_x[0]+1.25, control_point_y[0]+1.25),arrowprops=dict(facecolor='black', shrink=0.005))
# plt.annotateZ('End point', xy=(control_point_x[-1]+0.25, control_point_y[-1]+0.25), xytext=(control_point_x[-1]+1.25, control_point_y[-1]+1.25),arrowprops=dict(facecolor='black', shrink=0.005))
plt.title('B-Spline interpolation(Scipy & Implemented method)', fontsize=15)
plt.xlabel('x',horizontalalignment='center',fontsize=15)
plt.ylabel('y', horizontalalignment='center',fontsize=15)
# plt.plot(out[0], out[1], 'y',color='blue',label='Degree 3 Scipy method')
plt.plot(control_point_x_uniform, control_point_y_uniform,color='red',marker= 'D',label='Control Polygon(Uniform)',markersize=3)

plt.plot(control_point_x, control_point_y,color='darkgreen',marker= '.',linestyle='--',label='Control Polygon(Chord)',markersize=6)
plt.plot(inter_x,inter_y,linestyle='--',color='limegreen',label='Degree 3 B-Spline Curve(Chord)')
plt.plot(inter_x_uniform,inter_y_uniform,color='red',linestyle='--',label='Degree 3 B-Spline Curve(Uniform)')
plt.plot(x,y,'ko',label='Data Points',markersize=4)
plt.legend( bbox_to_anchor=(1.2, 0.3))
plt.tight_layout()
# plt.savefig('Comparison.png')
plt.show()