from discspring import *
from optimizer import *
from brute_force import *
import csv
import pandas as pd
import sys
import itertools

def run_Table(Data):
    Table = Data.values.tolist()
    Columns = Data.columns
    print(Columns)
    return

    now = datetime.now()
    folder_string = "results/" + file[:-4] + now.strftime("_%y%m%d_%H%M%S")
    Path(folder_string).mkdir(parents=True, exist_ok=True)

    for i in range(len(Table)):
        spring = DiscSpring(Table[i][0:6])
        spring.fileName = file

        max_s = 0.75 * spring.h0

        Table[i][6] = max_s
        Table[i][7] = spring.find_force(max_s)


        StressTable = np.zeros([100,5])
        for j in range(100):
            StressTable[j] = spring.find_stress(max_s*(j+1)/100)

        Table[i][8:13] = list(np.amax(StressTable, axis=0))
   
        plot_force(spring, folder_string, i)

    Output = pd.DataFrame(Table, columns=Columns)
    Output.to_csv(folder_string + "/" + file, index=False)


if __name__ == "__main__":
    file = "brute_columns.csv"

    Data = pd.read_csv(file)
    Columns = Data.columns

    #run_Table(Data)
    
    # optum =  Optimizer([210,140,8,4])
    # solution = optum.solution()

    # spring = DiscSpring(solution.x)

    #spring = DiscSpring([203,116,8,5.5])
    #max_s = 0.75 * spring.h0

    spring = SpringStack([203,116,8,5.5], "3S1P")

    folder_string = ("results/debug")
    plot_stack_force(spring,folder_string, 1)

    # print("Force:{}".format(spring.find_force(max_s)))
    # print("Rest-Force:{}".format(spring.find_force(max_s-1.5)))
    # print("Stress:{}".format(spring.find_stress(max_s)))

    # # folder_string = ("results/debug")
    # # plot_force(spring, folder_string, 0)
    

    # Input = "brute_input_2.csv"
    # Output = "brute_output_2.csv"
    # temp = bruteForce(Columns, Input, Output)
    

   









 