from discspring import *
from optimizer import *
import csv
import pandas as pd
import sys


if __name__ == "__main__":

    Data = pd.read_csv(sys.argv[1])
    Table = Data.values.tolist()
    Columns = Data.columns

    optum =  Optimizer([205,116,8,3,3,210000,3])
    solution = optum.solution()
    #solution = optum.brute()

    print(solution)


    # for i in range(len(Table)):
    #     spring = DiscSpring(Table[i][0:7])

    #     max_s = 0.75 * spring.h0

    #     Table[i][7] = max_s
    #     Table[i][8] = spring.find_force(max_s)
    #     Table[i][9:14] = spring.find_stress(max_s)

    #     spring.plot_force(0,max_s, i)

    # Output = pd.DataFrame(Table, columns=Columns)
    # Output.to_csv("spring_input.csv", index=False)
    

   









 