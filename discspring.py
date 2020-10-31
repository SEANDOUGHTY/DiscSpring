import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class DiscSpring:
    #t1 = t'
    def __init__(self, Input):
        self.D_e = Input[0]
        self.D_i = Input[1]
        self.I_o = Input[2]
        self.t = Input[3]
        self.t1 = self.t
        self.E = 210000
        self.mu = 0.3
        self.h0 = self.I_o - self.t
    
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
        B = (1/4) * (self.I_o/self.t) - (self.t1/self.t) + (3/4)
        C = (5/8) * (self.I_o/self.t) - (self.t1/self.t) + (3/8)
        
        return A/(B*C)
    
    def find_c2(self):
        A = self.C_1 / (self.t1/self.t)**3
        B = (5/32) * (self.I_o/self.t - 1)**2 + 1

        return A*B

    #Formula 8a
    def find_force(self, s):
        A = (4 * self.E) / (1 - self.mu**2)
        B = (self.t**4) / (self.K_1 * self.D_e**2)
        C = s / self.t
        D = (self.h0/self.t) - (s/self.t)
        E = (self.h0/self.t) - (s/(2*self.t))

        return A*B*C*(D*E + 1)

    def plot_force(self, number):
        s = np.linspace(0, self.h0, 100)
        F = np.zeros(100)

        for i in range(len(s)):
            F[i] = self.find_force(s[i])
 
        plt.plot(s,F, label='data')
        plt.axvline(x=self.h0, c='r', ls='--', label='Flat')
        plt.axvline(x=0.75*self.h0, c='y', ls='--', label='75% Flat')
        plt.axvline(x=0.75*self.h0 - 1.5, c='g', ls='--', label='Resting')
        plt.legend(loc="upper left")

        plt.xlabel("Displacement (mm)")
        plt.ylabel("Force (N)")
        plt.title("Run #{}. Spring Force Displacement Plot".format(number+1))
        plt.grid(which='major')

        plt.subplots_adjust(left=0.12, right=0.9, top=0.9, bottom=0.3)
        textstr = "teststr"
        plt.gcf().text(0.1, 0.16, "Outer Diameter (mm): %.1f" % self.D_e, fontsize=10)
        plt.gcf().text(0.1, 0.11, "Inner Diameter (mm): %.1f" % self.D_i, fontsize=10)
        plt.gcf().text(0.1, 0.06, "Uncompressed Height (mm): %.1f" % self.I_o, fontsize=10)
        plt.gcf().text(0.1, 0.01, "Thickness (mm): %.1f" % self.t, fontsize=10)

        plt.gcf().text(0.5, 0.16, 'Resting Force (N): %.1f' % self.find_force(self.h0*0.75 - 1.5), fontsize=10)
        plt.gcf().text(0.5, 0.11, "Loaded Force (N): %.1f" % self.find_force(self.h0*0.75), fontsize=10)
        plt.gcf().text(0.5, 0.06, "Max Stress (MPa): %.1f" % max(self.find_max_stress()), fontsize=10)
        

        plt.savefig("figures/run{}".format(number+1))
        plt.show()
        plt.close()
        

    def find_stress(self, s):
        stress = np.zeros(5)

        A = (4 * self.E)/(1 - self.mu**2)
        B = (self.t**2)/(self.K_1*self.D_e**2)
        C = self.K_4
        D = s/self.t
        E = 3/math.pi

        prefix = A*B*C*D #common to all stresses

        stress[0] = prefix * 3/math.pi
        stress[1] = prefix * \
            (self.K_4 * self.K_2 * (self.h0/self.t - s/(2*self.t)) + self.K_3)
        stress[2] = prefix * \
            (self.K_4 * self.K_2 * (self.h0/self.t - s/(2*self.t)) - self.K_3)
        stress[3] = prefix * (1 / self.delta) * \
            (self.K_4 * (self.K_2 - 2*self.K_3) * \
            (self.h0/self.t - s/(2*self.t)) - self.K_3)
        stress[4] = prefix * (1 / self.delta) * \
            (self.K_4 * (self.K_2 - 2*self.K_3) * \
            (self.h0/self.t - s/(2*self.t)) + self.K_3)

        return stress

    def find_max_stress(self):
        max_s = 0.75 * self.h0
        
        StressTable = np.zeros([100,5])
        for j in range(100):
            StressTable[j] = self.find_stress(max_s*(j+1)/100)
        

        max_stress = np.amax(StressTable, axis=0)

        
        return max_stress