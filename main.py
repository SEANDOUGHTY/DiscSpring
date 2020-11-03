from discspring import *
from optimizer import *
from brute_force import *
from datetime import datetime
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


if __name__ == "__main__":
    mode = "Brute"
      
    if mode == "Table":

        Data = pd.read_csv(file)
        Columns = Data.columns

        run_Table(Data)
            
    elif mode == "Spring":
        spring = DiscSpring([187,140,7.5,2.1, 1, 1], "Ti-6Al-4V", 108500, 0.34)
        max_s = 0.75 * spring.H_o

        now = datetime.now()
        folder_string = "results/run" + now.strftime("_%y%m%d_%H%M%S")
        Path(folder_string).mkdir(parents=True, exist_ok=True)

        plot_force(spring,0)
        plot_stress(spring, 0)

        print("Force:{}".format(spring.find_force(max_s)))
        print("Rest-Force:{}".format(spring.find_force(max_s-1.5)))
        print("Stress:{}".format(spring.find_stress(max_s)))

        
    
    elif mode == "Brute":
        
        file = "brute/brute_columns.csv"

        Data = pd.read_csv(file)
        Columns = Data.columns

        Input = "brute/brute_input_10_Aluminum.csv"
        Output = "brute/brute_output_10_Aluminum.csv"
        temp = bruteForce(Columns, Input, Output, Material="Aluminum 7075", E=72000, mu=0.33, Max_Stress=420)

        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(Input, 'discspring-output', Input, ExtraArgs={'ACL': 'public-read'})
        s3.meta.client.upload_file(Output, 'discspring-output', Output, ExtraArgs={'ACL': 'public-read'})
        url = "https://discspring-output.s3.amazonaws.com/" + Input
        print(url)
        url = "https://discspring-output.s3.amazonaws.com/" + Output
        print(url)
    

   









 