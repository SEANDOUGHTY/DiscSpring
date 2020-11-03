import numpy as np
import itertools
from discspring import *
import pandas as pd
import progressbar



def bruteForce(Columns, Input_File, Output_File, Material, E, mu, Max_Stress):

    Data = pd.read_csv(Input_File, header=None)
    Options = Data.values.tolist()

    for i in range(len(Options)):
        for j in range(len(Options[i])):
            if Options[i][j] != Options[i][j]:
                Options[i] = Options[i][:j]
                break
            
    all_possibility = list(itertools.product(*Options))
    print(len(all_possibility))
    
    Table = []

    for i in range(len(all_possibility)):
    #for i in range(1000):
        spring = DiscSpring(all_possibility[i], Material, E, mu)
        
        if spring.H_o <= 0:
            continue

        max_s = 0.75 * spring.H_o

        spring_row = [spring.D_e, spring.D_i, spring.l_o, spring.t, spring.n_series, spring.n_parallel,\
            spring.E, spring.mu, spring.H_o, spring.L_o ,max_s,\
            spring.find_force(max_s-1.5), spring.find_force(max_s), spring.find_stress(max_s)[0], spring.find_stress(max_s)[1],\
            spring.find_stress(max_s)[2], spring.find_stress(max_s)[3], spring.find_stress(max_s)[4],\
            max_stress_constraint(spring, Max_Stress), spring.delta, rec_1_const(spring), spring.H_o/spring.t, rec_2_const(spring),\
            spring.D_e/spring.t, rec_3_const(spring), (spring.H_o * 0.75 - 1.5)/spring.H_o, preload_const(spring)]

        
        spring_row = [round(num, 2) if type(num) != type(True) else num for num in spring_row ]
        
        Table.append(spring_row)

        if i % 1000 == 0:
           print(str((i/len(all_possibility))*100) + "%")

    Output = pd.DataFrame(Table, columns=Columns)
    Output.to_csv(Output_File, index=True)

def max_stress_constraint(spring, Max_Stress):
    max_s = 0.75 * spring.H_o
    if max(abs(spring.find_stress(max_s))) < Max_Stress:
        return True
    else:
        return False

def rec_1_const(spring):
    if spring.delta < 1.75:
        return False
    if spring.delta > 2.5:
        return False
    return True

def rec_2_const(spring):
    if spring.h_o/spring.t < 0.4:
        return False
    if spring.h_o/spring.t > 1.3:
        return False
    return True

def rec_3_const(spring):
    if spring.D_e/spring.t < 16:
        return False
    if spring.D_e/spring.t > 40:
        return False
    return True

def preload_const(spring):
    if (spring.h_o <= 0):
        return False
    if (spring.h_o * 0.75 - 1.5)/spring.h_o > 0.15:
        return True
    return False
    