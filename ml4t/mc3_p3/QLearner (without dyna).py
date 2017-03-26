"""
Template for implementing QLearner  (c) 2015 Tucker Balch
implement by ztz
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        #initialize Q
        self.Q = np.random.uniform(-1.0,1.0,size = (self.num_states,self.num_actions))

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        rarkey = np.random.random()
        if rarkey > self.rar:
            action = np.argmax(self.Q[self.s,:])
        else:
            action = rand.randint(0, self.num_actions-1)
               
        self.a = action
        
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        
        #update Q
        self.Q[self.s,self.a] = ((1-self.alpha)*self.Q[self.s,self.a])+self.alpha*(r+self.gamma*self.Q[s_prime,:].max())

        self.s = s_prime
        rarkey = np.random.random()
        if rarkey > self.rar:
            action = np.argmax(self.Q[self.s,:])
        else:
            action = rand.randint(0, self.num_actions-1)
        
        self.rar = self.rar*self.radr
        self.a = action

        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        if self.verbose: print self.rar
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"


    
        
    
