from discspring import *
import numpy as np
import csv
import pandas as pd

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

        max_s = 0.75 * spring.h_o

        Table[i][6] = max_s
        Table[i][7] = spring.find_force(max_s)


        StressTable = np.zeros([100,5])
        for j in range(100):
            StressTable[j] = spring.find_stress(max_s*(j+1)/100)

        Table[i][8:13] = list(np.amax(StressTable, axis=0))
   
        plot_force(spring, folder_string, i)

    Output = pd.DataFrame(Table, columns=Columns)
    Output.to_csv(folder_string + "/" + file, index=False)