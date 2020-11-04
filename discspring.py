import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from pathlib import Path
import boto3


class DiscSpring:
    #t1 = t'
    def __init__(self, Input, Material, E, mu):
        self.fileName = "" #default value to be overwritten
        self.D_e = Input[0]
        self.D_i = Input[1]
        self.l_o = Input[2]
        self.t = Input[3]
        
        #Paralell Series
        self.n_series = Input[4]
        self.n_parallel = Input[5]
        
        #Formula 25
        self.L_o = self.n_series * (self.l_o + (self.n_parallel - 1)*self.t)
        
        self.t1 = self.t
        self.E = E
        self.mu = mu
        self.Material = Material
        
        self.h_o = self.l_o - self.t
        self.H_o = self.n_series * (self.h_o)
    
        #Formula 1 (Find center of rotation during deflection)
        self.D_o = (self.D_e - self.D_i)/(math.log(self.D_e)/self.D_i)

        #Formula 2
        self.delta = self.D_e/self.D_i

        self.C_1 = self.find_c1()
        self.C_2 = self.find_c2()    

        self.K_1 = self.find_k1()
        self.K_2 = self.find_k2()
        self.K_3 = self.find_k3()
        self.K_4 = self.find_k4()


    #Formula 3
    def find_k1(self):
        num = ((self.delta - 1)/(self.delta))**2
        den = (self.delta + 1)/(self.delta -1) - 2/(math.log(self.delta))
        
        return num/(math.pi * den)

    #Formula 4
    def find_k2(self):
        num = (self.delta - 1)/math.log(self.delta) - 1
        den = (math.log(self.delta))

        return (6*num)/(math.pi * den)

    #Formula 5
    def find_k3(self):
        return (3 * (self.delta - 1))/(math.pi * math.log(self.delta))

    #Formula 6
    def find_k4(self):
        n1 = (self.C_1 / 2)**2 + self.C_2
        n2 = -self.C_1 / 2 + math.sqrt(n1)
        return math.sqrt(n2)
        
    def find_c1(self):
        #C_1 = A/(B*C)        
        A = (self.t1 / self.t)**2
        B = (1/4) * (self.l_o/self.t) - (self.t1/self.t) + (3/4)
        C = (5/8) * (self.l_o/self.t) - (self.t1/self.t) + (3/8)
        
        if B*C == 0:
            return 0

        return A/(B*C)
    
    def find_c2(self):
        A = self.C_1 / (self.t1/self.t)**3
        B = (5/32) * (self.l_o/self.t - 1)**2 + 1

        return A*B

    #Formula 8a
    def find_force(self, s_ges):
        s = s_ges/self.n_series

        A = (4 * self.E) / (1 - self.mu**2)
        B = (self.t**4) / (self.K_1 * self.D_e**2)
        C = s / self.t
        D = (self.h_o/self.t) - (s/self.t)
        E = (self.h_o/self.t) - (s/(2*self.t))

        return A*B*C*(D*E + 1)*self.n_parallel      

    def find_stress(self, s_ges):
        s = s_ges/self.n_series

        stress = np.zeros(5)

        A = (4 * self.E)/(1 - self.mu**2)
        B = (self.t**2)/(self.K_1*self.D_e**2)
        C = self.K_4
        D = s/self.t
        E = 3/math.pi

        prefix = -A*B*C*D #common to all stresses

        stress[0] = prefix * 3/math.pi
        stress[1] = prefix * \
            (self.K_4 * self.K_2 * (self.h_o/self.t - s/(2*self.t)) + self.K_3)
        stress[2] = prefix * \
            (self.K_4 * self.K_2 * (self.h_o/self.t - s/(2*self.t)) - self.K_3)
        stress[3] = prefix * (1 / self.delta) * \
            (self.K_4 * (self.K_2 - 2*self.K_3) * \
            (self.h_o/self.t - s/(2*self.t)) - self.K_3)
        stress[4] = prefix * (1 / self.delta) * \
            (self.K_4 * (self.K_2 - 2*self.K_3) * \
            (self.h_o/self.t - s/(2*self.t)) + self.K_3)

        return stress


def plot_force(spring, run_number, folder=None):
    s_ges = np.linspace(0, spring.H_o, 100)
    F = np.zeros(100)

    for i in range(len(s_ges)):
        F[i] = spring.find_force(s_ges[i])

    plt.plot(s_ges,F, label='Force')
    plt.axvline(x=spring.h_o, c='r', ls='--', label='Flat')
    plt.axvline(x=0.75*spring.h_o, c='y', ls='--', label='Loaded')
    plt.axvline(x=0.75*spring.h_o - 1.5, c='g', ls='--', label='Resting')
    plt.legend(loc="upper left")

    plt.xlabel("Displacement (mm)")
    plt.ylabel("Force (N)")
    plt.title("Run #{}. Spring Force Displacement Plot".format(run_number+1))
    plt.grid(which='major')

    plt.subplots_adjust(left=0.12, right=0.9, top=0.9, bottom=0.40)
    plt.gcf().text(0.1, 0.26, "Outer Diameter (mm): %.1f" % spring.D_e, fontsize=10)
    plt.gcf().text(0.1, 0.21, "Inner Diameter (mm): %.1f" % spring.D_i, fontsize=10)
    plt.gcf().text(0.1, 0.16, "Uncompressed Height (mm): %.1f" % spring.l_o, fontsize=10)
    plt.gcf().text(0.1, 0.11, "Single Thickness (mm): %.1f" % spring.t, fontsize=10)
    plt.gcf().text(0.1, 0.06, "Young's Modulus (MPa): %.0f" % spring.E, fontsize=10)
    plt.gcf().text(0.1, 0.01, "Number Series:  %.0f" % spring.n_series, fontsize=10)

    plt.gcf().text(0.5, 0.26, 'Resting Force (N): %.1f' % spring.find_force(spring.h_o*0.75 - 1.5), fontsize=10)
    plt.gcf().text(0.5, 0.21, "Loaded Force (N): %.1f" % spring.find_force(spring.h_o*0.75), fontsize=10)
    plt.gcf().text(0.5, 0.16, "Loaded Max Stress (MPa): %.1f" % max(abs(spring.find_stress(spring.h_o*0.75))), fontsize=10)
    plt.gcf().text(0.5, 0.11, "Material: {}".format(spring.Material), fontsize=10)
    plt.gcf().text(0.5, 0.06, "Poisson's Ratio: %.2f" % spring.mu, fontsize=10)
    plt.gcf().text(0.5, 0.01, "Number Parallel: %.0f" % spring.n_parallel, fontsize=10)
    
    fig = plt.gcf()
    fig.set_size_inches(9, 6)

    if folder != None:
        file = "{}/force_run{}.png".format(folder, run_number+1)
        fig.savefig(file)

        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(file, 'discspring-output', file, ExtraArgs={'ACL': 'public-read'})
        url = "https://discspring-output.s3.amazonaws.com/" + file
        print(url)

    plt.show()
    plt.close()

def plot_stress(spring, run_number, folder=None):
    s_ges = np.linspace(0, spring.H_o, 100)
    Stress = np.zeros([100,5])

    for i in range(len(s_ges)):
        Stress[i] = spring.find_stress(s_ges[i])
    Stress = np.absolute(Stress)

    plt.plot(s_ges,Stress, label=("data", "data") )
    plt.axvline(x=spring.h_o, c='r', ls='--', label='Flat')
    plt.axvline(x=0.75*spring.h_o, c='y', ls='--', label='75% Flat')
    plt.axvline(x=0.75*spring.h_o - 1.5, c='g', ls='--', label='Resting')
    plt.legend(('Comp. Stress OM', 'Comp. Stress 1', 'Tens. Stress 2', 'Tens. Stress 3', \
        'Comp. Stress 4', 'Flat', 'Loaded', 'Resting'), loc="upper left")

    
    plt.xlabel("Displacement (mm)")
    plt.ylabel("Stress (MPa)")
    plt.title("Run #{}. Spring Stress Plot".format(run_number+1))
    plt.grid(which='major')

    plt.subplots_adjust(left=0.12, right=0.9, top=0.9, bottom=0.40)
    plt.gcf().text(0.1, 0.26, "Outer Diameter (mm): %.1f" % spring.D_e, fontsize=10)
    plt.gcf().text(0.1, 0.21, "Inner Diameter (mm): %.1f" % spring.D_i, fontsize=10)
    plt.gcf().text(0.1, 0.16, "Uncompressed Height (mm): %.1f" % spring.l_o, fontsize=10)
    plt.gcf().text(0.1, 0.11, "Single Thickness (mm): %.1f" % spring.t, fontsize=10)
    plt.gcf().text(0.1, 0.06, "Young's Modulus (MPa): %.0f" % spring.E, fontsize=10)
    plt.gcf().text(0.1, 0.01, "Number Series:  %.0f" % spring.n_series, fontsize=10)

    plt.gcf().text(0.5, 0.26, 'Resting Force (N): %.1f' % spring.find_force(spring.h_o*0.75 - 1.5), fontsize=10)
    plt.gcf().text(0.5, 0.21, "Loaded Force (N): %.1f" % spring.find_force(spring.h_o*0.75), fontsize=10)
    plt.gcf().text(0.5, 0.16, "Loaded Max Stress (MPa): %.1f" % max(abs(spring.find_stress(spring.h_o*0.75))), fontsize=10)
    plt.gcf().text(0.5, 0.11, "Material: {}".format(spring.Material), fontsize=10)
    plt.gcf().text(0.5, 0.06, "Poisson's Ratio: %.2f" % spring.mu, fontsize=10)
    plt.gcf().text(0.5, 0.01, "Number Parallel: %.0f" % spring.n_parallel, fontsize=10)
    
    fig = plt.gcf()
    fig.set_size_inches(9, 6)

    if folder != None:
        file = "{}/stress_run{}.png".format(folder, run_number+1)
        fig.savefig(file)

        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(file, 'discspring-output', file, ExtraArgs={'ACL': 'public-read'})
        url = "https://discspring-output.s3.amazonaws.com/" + file
        print(url)

    plt.show()
    plt.close()