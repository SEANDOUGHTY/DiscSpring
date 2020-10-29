from diskspring import *
import csv
import pandas as pd


if __name__ == "__main__":

    Data = pd.read_csv("spring_input.csv")
    Table = Data.values.tolist()
    Columns = Data.columns

    for i in range(len(Table)):
        spring = DiscSpring(Table[i][0:7])

        max_s = 0.75 * spring.h0

        Table[i][7] = max_s
        Table[i][8] = spring.find_force(max_s)
        Table[i][9:14] = spring.find_stress(max_s)

        spring.plot_force(0,max_s, i)

    Output = pd.DataFrame(Table, columns=Columns)
    Output.to_csv("spring_input.csv", index=False)
    

   







 