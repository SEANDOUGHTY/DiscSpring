from discspring import *
from optimizer import *
from brute_force import *
from datetime import datetime
import csv
import pandas as pd
import sys
import itertools

if __name__ == "__main__":
    mode = "Spring"

    #Deprecated function  
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

        plot_force(spring, 0, folder_string)
        plot_stress(spring, 0, folder_string)

        print("Force:{}".format(spring.find_force(max_s)))
        print("Rest-Force:{}".format(spring.find_force(max_s-1.5)))
        print("Stress:{}".format(spring.find_stress(max_s)))


    elif mode == "Brute":
        
        #Import Column Format
        file = "columns.csv"
        Data = pd.read_csv(file) 
        Columns = Data.columns

        #Define Input and Outut Formats
        Input = "brute/brute_input_11_Titanium.csv"
        Output = "brute/brute_output_11_Titanium.csv"
        temp = bruteForce(Columns, Input, Output, Material="Ti-6Al-4V", E=104800, mu=0.31, Max_Stress=690)

        #Save and Upload to AWS
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(Input, 'discspring-output', Input, ExtraArgs={'ACL': 'public-read'})
        s3.meta.client.upload_file(Output, 'discspring-output', Output, ExtraArgs={'ACL': 'public-read'})
        url = "https://discspring-output.s3.amazonaws.com/" + Input
        print(url)
        url = "https://discspring-output.s3.amazonaws.com/" + Output
        print(url)
    

   









 