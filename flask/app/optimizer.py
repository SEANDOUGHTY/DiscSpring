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
        self.con3 = {'type': 'ineq', 'fun': self.preload_constraint}
        self.con4 = {'type': 'ineq', 'fun': self.recommend1_min}
        self.con5 = {'type': 'ineq', 'fun': self.recommend1_max}
        self.con6 = {'type': 'ineq', 'fun': self.recommend2_min}
        self.con7 = {'type': 'ineq', 'fun': self.recommend2_max}
        
        self.cons = [self.con1, self.con2, self.con3, self.con4, self.con5, self.con6, self.con7]
        
     
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
        max_stress = spring.find_max_stress()

        return allowable_stress - max_stress

    def curve_constraint(self, guess):
        #Constrains spring characteristic curve above specified value (h_o/t)
        min_curve_constant = 1.4
        spring = DiscSpring(guess)
        curve_constant = spring.h0/spring.t

        return curve_constant - min_curve_constant

    def preload_constraint(self, guess):
        min_preload = 0.15 #percent
        spring = DiscSpring(guess)
        preload = (spring.h0 * 0.75 - 1.5)/spring.h0

        return  preload - min_preload

    #Recommendation for the Delta Value
    def recommend1_min(self, guess):
        min_delta = 1.75
        spring = DiscSpring(guess)

        return spring.delta - min_delta

    def recommend1_max(self, guess):
        max_delta = 2.5
        spring = DiscSpring(guess)

        return max_delta - spring.delta

    #Recommendations for h_0/t
    def recommend2_min(self, guess):
        min_recommend = 0.4
        spring = DiscSpring(guess)

        return spring.h0/spring.t - min_recommend

    def recommend2_max(self, guess):
        max_recommend = 1.3
        spring = DiscSpring(guess)

        return max_recommend - spring.h0/spring.t


    def solution(self):
        #Least Squares Optimizer
        solution = minimize(self.objective, self.inital_guess, method='SLSQP',\
            bounds=self.bnds, constraints=self.cons)
        
        
        print(solution)
        return solution