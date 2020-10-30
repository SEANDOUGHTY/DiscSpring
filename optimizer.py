from discspring import *
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Optimizer():
    def __init__(self, inital_guess):
        self.inital_guess = inital_guess
        self.bnds = ((205,205),(116,116),(4,8),(0.3,5),(0.3,5),(210000,210000),(0.3,0.3))
        self.con1 = {'type': 'ineq', 'fun': self.force_constraint}
        self.con2 = {'type': 'ineq', 'fun': self.displacement_constraint}
        self.cons = [self.con1, self.con2]
     
    def objective(self, guess):
        spring = DiscSpring(guess)
        max_s = 0.75 * spring.h0
        max_stress = abs(max(spring.find_stress(max_s)))

        return max_stress

    def force_constraint(self, guess):
        spring = DiscSpring(guess)
        max_s = 0.75 * spring.h0
        max_force = spring.find_force(max_s)
        desired_force = 3000

        return max_s - desired_force

    def displacement_constraint(self, guess):
        spring = DiscSpring(guess)
        max_s = 0.75 * spring.h0

        return max_s - 4.5

    def solution(self):
        solution = minimize(self.objective, self.inital_guess, method='SLSQP',\
            bounds=self.bnds, constraints=self.cons)

        print(solution)
        return solution