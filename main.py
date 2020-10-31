from discspring import *
from optimizer import *
import csv
import pandas as pd
import sys


if __name__ == "__main__":

    Data = pd.read_csv("spring_input_2.csv")
    Table = Data.values.tolist()
    Columns = Data.columns

    # optum =  Optimizer([210,140,8,3])
    # solution = optum.solution()

    # spring = DiscSpring([210,117,6.3,2.1])
    # max_s = 0.75 * spring.h0

    # print("Force:{}".format(spring.find_force(max_s)))
    # print("Rest-Force:{}".format(spring.find_force(max_s-1.5)))
    # print("Stress:{}".format(spring.find_stress(max_s)))

    # spring.plot_force(0)



    for i in range(len(Table)):
        spring = DiscSpring(Table[i][0:6])

        max_s = 0.75 * spring.h0

        Table[i][6] = max_s
        Table[i][7] = spring.find_force(max_s)


        StressTable = np.zeros([100,5])
        for j in range(100):
            StressTable[j] = spring.find_stress(max_s*(j+1)/100)

        Table[i][8:13] = list(np.amax(StressTable, axis=0))

        spring.plot_force(i)

    Output = pd.DataFrame(Table, columns=Columns)
    Output.to_csv("spring_input_2.csv", index=False)
    

   









 