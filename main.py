import os
import numpy as np
import math
from scipy.linalg import lu
from numpy.linalg import solve

def basis(t_list,u_list):
    n=len(t_list)-1
    N=np.zeros([n+3,n+3])
    count=0
    for i in range(n+1):
        idx_i=i+1
        for j in range(n+3):
            N[idx_i][j]=compute(u_list[j:j+5],t_list[i])
            # print(N[idx_i][j])
        # print(idx_i)
    '''Endpoints condition'''
    for i in range(2):
        for j in range(n+3):
            N[i*(n+2)][j]=endpoint_conditions(u_list[j:j+5],t_list[i*(n)])
    np.set_printoptions(suppress=True,precision=2)

    print(N)
    return N

def compute(u,t,flag=None):
    '''u is a list of degree+1 , t is the substitute value'''
    value=0
    u_0=u[0]
    u_1=u[1]
    u_2=u[2]
    u_3=u[3]
    u_4=u[4]

    if u_3 <= t and t<=u_4 and (t!=u_3 or t!=u_4):
        value = (((u_4 - t) ** 3)) / ((u_4 - u_3) * (u_4 - u_2) * (u_4 - u_1))
    elif u_2<=t and u_3>t and (t!=u_2 or t!=u_3):
        value=((t-u_0)*((u_3-t)**2))/((u_3-u_2)*(u_3-u_1)*(u_3-u_0))+((u_4-t)*(u_3-t)*(t-u_1))/((u_3-u_2)*(u_4-u_1)*(u_3-u_1))
        +((((u_4-t)**2)*(t-u_2))/((u_3-u_2)*(u_4-u_2)*(u_4-u_1)))
    elif u_1<=t and u_2>t and (t!=u_1 or t!=u_2):
        value=(((t-u_0)**2)*(u_2-t))/((u_2-u_1)*(u_3-u_0)*(u_2-u_0))+((u_3-t)*(t-u_0)*(t-u_1))/((u_2-u_1)*(u_3-u_1)*(u_3-u_0))
        +(((u_4-t)*((t-u_1)**2))/((u_2-u_1)*(u_4-u_1)*(u_3-u_1)))
    elif u_0<=t and u_1>=t and (t!=u_0 or t!=u_1):
        value=((t-u_0)**3)/((u_1-u_0)*(u_2-u_0)*(u_3-u_0))

    if math.isnan(value) or math.isinf(value):
        value=0

    return value
def endpoint_conditions(u,t):
    '''u is a list of degree+1 , t is the substitute value'''
    value = 0
    u_0 = u[0]
    u_1 = u[1]
    u_2 = u[2]
    u_3 = u[3]
    u_4 = u[4]
    count=0

    if u_3 <= t and t <= u_4 and (t != u_3 or t != u_4):
        value = (6*(u_4 - t)) / ((u_4 - u_3) * (u_4 - u_2) * (u_4 - u_1))
        count+=1
        print('con4!input ={} range=[{},{}] value={}'.format(t,u_3,u_4,value))
    elif u_2 <= t and u_3 >= t and (t != u_2 or t != u_3):
        value = ((6*t-4*u_3-2*u_0) / ((u_3 - u_2) * (u_3 - u_1) * (u_3 - u_0))) + ((
                    6*t-2*u_1-2*u_3-2*u_4) / ((u_3 - u_2) * (u_4 - u_1) * (u_3 - u_1))) +((6*t-4*u_4-2*u_2) / ((u_3 - u_2) * (u_4 - u_2) * (u_4 - u_1)))
        count+=1
        print('con3!input ={} range=[{},{}] value={}'.format(t,u_2,u_3,value))

    elif u_1 <= t and u_2 >=t and (t != u_1 or t != u_2):
        value = ((2*u_2-6*t+4*u_0) / ((u_2 - u_1) * (u_3 - u_0) * (u_2 - u_0)) )+ ((2*u_1+2*u_0+2*u_3-6*t) / ((u_2 - u_1) * (u_3 - u_1) * (u_3 - u_0))) +((-6*t+4*u_1+2*u_4) / ((u_2 - u_1) * (u_4 - u_1) * (u_3 - u_1)))
        count+=1
        print('con2!input ={} range=[{},{}] value={}'.format(t,u_1,u_2,value))

    elif u_0 <= t and u_1 >= t and (t != u_0 or t != u_1):
        value = (6*(t - u_0) ) / ((u_1 - u_0) * (u_2 - u_0) * (u_3 - u_0))
        count+=1
        print('con1!input ={} range=[{},{}] value={}'.format(t,u_0,u_1,value))

    if math.isnan(value) or math.isinf(value):
        value = 0
    print('final!input ={} value={}'.format(t,value))

    return value
def param(data,type='chord'):
    dist_list=[]
    accu_dist_list=[]
    t_list=[]
    u_list=[]
    n=len(data)-1
    k=1
    count=1
    dist=0

    if type=='chord':
        '''Chord Length Parameterization'''
        print('Chord Length Parameterization')
        while count<=n:
            vec1=np.array(data[count])
            vec2=np.array(data[count-1])
            new_dist=np.linalg.norm(vec1 - vec2)
            dist +=new_dist
            dist_list.append(new_dist)
            accu_dist_list.append(dist)
            count += 1

        dist_sum=sum(dist_list)
        count=0
        # print(dist_list)
        while count<n+7:
            if count<4:
                u_list.append(0)
            elif count>=n+3:
                u_list.append(1)
            else:
                u_list.append(accu_dist_list[count-4]/dist_sum)
            count+=1

        count=0
        while count<n+1:
            if count<1:
                t_list.append(0)
            elif count>=n:
                t_list.append(1)
            else:
                t_list.append(accu_dist_list[count-1]/dist_sum)
            count+=1
    else:
        print('Uniform Parameterization')
        count=0
        while count<n+1:
            if count<1:
                t_list.append(0)
            elif count>=n:
                t_list.append(1)
            else:
                t_list.append(count/n)
            count+=1

        count=0
        while count < n + 7:
            if count < 3:
                u_list.append(0)
            elif count >= n + 3:
                u_list.append(1)
            else:
                u_list.append(t_list[count-3])
            count+=1

    return t_list,u_list



if __name__ == '__main__':
    degree=3
    data = []
    with open("example1.txt", "rt") as file:
        for line in file:
            data.append(list(map(int,line.strip().split(" "))))


    n=len(data)-1
    knots_len=n+7
    control_points_num=knots_len-degree-1

    t_list,u_list=param(data,type='chord')
    N=basis(t_list,u_list)
    x_list=[]
    y_list=[]
    x_list.append(0)
    y_list.append(0)
    for points in data:
        x_list.append(points[0])
        y_list.append(points[1])
    x_list.append(0)
    y_list.append(0)

    control_points_x_list=solve(N, x_list)
    control_points_y_list=solve(N, y_list)
    control_points_x_list[abs(control_points_x_list)<((np.e)**(-10))]=0.0
    control_points_y_list[abs(control_points_y_list)<((np.e)**(-10))]=0.0

    # print(data)

    for x, y in zip(control_points_x_list, control_points_y_list):
        print('['+str(round(x,2)) + " " + str(round(y,2)) + ']')
    with open("example1_output_chord.txt", "wt") as output:
        output.write(str(degree)+'\n')
        output.write(str(len(control_points_x_list))+'\n')
        output.write('\n')
        for knots in u_list:
            output.write(str(knots)+' ')

        output.write('\n')
        output.write('\n')
        for x,y in zip(control_points_x_list,control_points_y_list):
            output.write(str(x)+" "+str(y)+'\n')
