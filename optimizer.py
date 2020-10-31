from discspring import *
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Optimizer():
    def __init__(self, inital_guess):
        self.inital_guess = inital_guess
        self.bnds = ((197,210),(116,140),(5.5,11),(0.5,6))
        self.con1 = {'type': 'ineq', 'fun': self.stress_constraint}
        self.con2 = {'type': 'ineq', 'fun': self.curve_constraint}
        
        self.cons = [self.con1, self.con2]
        
     
    def objective(self, guess):
        #Objective: reach target force specified
        target_force = 3000

        spring = DiscSpring(guess)
        max_s = 0.75 * spring.h0
        resting_s = max_s - 1.5
        brake_force = spring.find_force(resting_s)

        return math.sqrt((brake_force - target_force)**2)

    def stress_constraint(self, guess):
        #Stress: Keep max stresses below the allowable stress in MPa
        allowable_stress = 600 

        spring = DiscSpring(guess)
        # max_s = 0.75 * spring.h0
        
        # StressTable = np.zeros([100,5])
        # for i in range(100):
        #     StressTable[i] = spring.find_stress(max_s*(i+1)/100)

        max_stress = spring.find_max_stress()

        return allowable_stress - max_stress

    def curve_constraint(self, guess):
        #Constrains spring characteristic curve above specified value (h_o/t)
        min_curve_constant = 1.4
        spring = DiscSpring(guess)
        curve_constant = spring.h0/spring.t

        return curve_constant - min_curve_constant

    def solution(self):
        #Least Squares Optimizer
        solution = minimize(self.objective, self.inital_guess, method='SLSQP',\
            bounds=self.bnds, constraints=self.cons)
        
        
        print(solution)
        return solution