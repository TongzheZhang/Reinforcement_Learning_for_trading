"""
ztz: BagLearner

learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":3}, bags = 20, boost = False, verbose = False)
learner.addEvidence(Xtrain, Ytrain)
Y = learner.query(Xtest)
"""

import numpy as np
import KNNLearner as knn
import LinRegLearner as lrl



class BagLearner(object):

    def __init__(self, learner, kwargs = {"k":3}, bags = 20, boost = False, verbose = False):
        
        self.learner = learner
        self.verbose = verbose
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.k = kwargs["k"]
        if learner == knn.KNNLearner:
            if verbose == True:
                print 'bag KNN test'
            self.learner = learner(k = self.k, verbose = self.verbose)
        if learner == lrl.LinRegLearner:
            if verbose == True:
                print "Lin BAG test"
            self.learner = learner(verbose = self.verbose)
            
    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        
        self.trainX = dataX
        self.trainY = dataY
        self.ran_idx = np.zeros([self.bags,dataX.shape[0]],dtype = int)
        for b in range(0,self.bags):
            self.ran_idx[b] = np.random.randint(0,dataX.shape[0],dataX.shape[0])
        if self.verbose == True:
            print "self.ran_idx.shape: ",self.ran_idx.shape

    def query(self,dataX):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """

        sumY = np.zeros(dataX.shape[0])
        predY = np.zeros(dataX.shape[0])
        for b in range(0,self.bags):
            newX = self.trainX[self.ran_idx[b]]
            newY = self.trainY[self.ran_idx[b]]
            self.learner.addEvidence(newX,newY)
            predY = self.learner.query(dataX)
            sumY  = sumY + predY 
                
            
        return sumY/self.bags
if __name__=="__main__":
    '''
    test1 = np.array([1,2,4,7])
    test2 = np.random.randint(1,2,3)    
    indices = np.array([1,1,1])
    test3 = test1[test2]
    print test1
    print test3
    print indices
    print
    '''
    print "the secret clue is 'zzyzx ' from BagLearner "