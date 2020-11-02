import numpy as np
import itertools
from discspring import *
import pandas as pd



def bruteForce(Columns, Input_File, Output_File):

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
        spring = DiscSpring(all_possibility[i])
        
        if spring.h0 <= 0:
            continue

        max_s = 0.75 * spring.h0

        spring_row = [spring.D_e, spring.D_i, spring.I_o, spring.t, spring.E, spring.mu,\
            spring.h0 ,max_s,\
            spring.find_force(max_s-1.5), spring.find_force(max_s), spring.find_max_stress()[0], spring.find_max_stress()[1],\
            spring.find_max_stress()[2], spring.find_max_stress()[3], spring.find_max_stress()[4],\
            max_stress_constraint(spring), spring.delta, rec_1_const(spring), spring.h0/spring.t, rec_2_const(spring),\
            spring.D_e/spring.t, rec_3_const(spring), (spring.h0 * 0.75 - 1.5)/spring.h0, preload_const(spring)]

        #spring_row = [round(num, 1) for num in spring_row]
        Table.append(spring_row)
        
        if i % 100 == 0:
            print(str((i/len(all_possibility))*100) + "%")
        

    Output = pd.DataFrame(Table, columns=Columns)
    Output.to_csv(Output_File, index=True)

def max_stress_constraint(spring):
    if max(abs(spring.find_max_stress())) < 600:
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
    if spring.h0/spring.t < 0.4:
        return False
    if spring.h0/spring.t > 1.3:
        return False
    return True

def rec_3_const(spring):
    if spring.D_e/spring.t < 16:
        return False
    if spring.D_e/spring.t > 40:
        return False
    return True

def preload_const(spring):
    if (spring.h0 <= 0):
        return False
    if (spring.h0 * 0.75 - 1.5)/spring.h0 > 0.15:
        return True
    return False
    