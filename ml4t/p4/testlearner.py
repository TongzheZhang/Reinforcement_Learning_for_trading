"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import KNNLearner as knn
import BagLearner as bl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

if __name__=="__main__":
    
    # read data, create data
    inf = open('data/ripple.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]
 
    '''ztz: plot 3D dataset
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = data[:600,0]
    y = data[:600,1]
    z = data[:600,2]
    x1 = data[600:,0]
    y1 = data[600:,1]
    z1 = data[600:,2]
    ax.scatter(x,y,z,c = 'r',marker = 'o')
    ax.scatter(x1,y1,z1,c = 'b',marker = 'v')
    ax.set_xlabel('X1 Label')
    ax.set_ylabel('X2 Label')
    ax.set_zlabel('Y Label')
    plt.show()

    #ztz:Test!!!!!
    # read data, create data
    inf = open('data/ripple.csv')
    traindata = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    inf = open('data/testcase10.csv')
    testdata = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    #train_rows = math.floor(0.6* data.shape[0])
    #test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = traindata[:,0:-1]
    trainY = traindata[:,-1]
    testX = testdata[:,0:-1]
    testY = testdata[:,-1]
    '''
    
    '''
    # 1.test LinRegLearner
    # create a learner and train it
    learner = lrl.LinRegLearner(verbose = False) # create a LinRegLearner
    learner.addEvidence(trainX, trainY) # train it

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]
    '''
    

    
    '''
    # 2.test KNNLearner
        print "k: ",i
        learner = knn.KNNLearner(k = i, verbose = False)
        learner.addEvidence(trainX,trainY)
    
    # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        print "KNN: "
        print "In sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(predY, y=trainY)
        print "corr: ", c[0,1]
        out[i-1,0] = rmse
        out[i-1,1] = c[0,1]
        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        print
        print "Out of sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(predY, y=testY)
        print "corr: ", c[0,1]
        out[i-1,2] = rmse
        out[i-1,3] = c[0,1]
        
    #print out
    #print out[:,1]
    '''
    
    
    # 3.test Bagging
    
    out = np.empty((20,4),dtype = float)
    print out.shape
    for i in range(1,21):
        learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":i}, bags = 20, boost = False,
        verbose = False)
        learner.addEvidence(trainX, trainY)
        print i
    # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        #print "BagLearner: "
        #print "In sample results"
        #print "RMSE: ", rmse
        c = np.corrcoef(predY, y=trainY)
        #print "corr: ", c[0,1]
        out[i-1,0] = rmse
        out[i-1,1] = c[0,1]
    # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        print
        #print "Out of sample results"
        #print "RMSE: ", rmse
        c = np.corrcoef(predY, y=testY)
        print "corr: ", c[0,1] 
        out[i-1,2] = rmse
        out[i-1,3] = c[0,1]
    plt.xlabel("K")
    plt.ylabel("Corr")
    plt.plot(out[:,1], 'r^', label = "In sample results")
    plt.plot(out[:,3], 'bs', label = "Out sample results")
    plt.plot(out[:,1], 'r', out[:,3], 'b')
    plt.title("# of K vs Corr by ripple.csv")
    plt.legend()
    plt.show()
    
    #learners = []
    #for i in range(0,10):
        #kwargs = {"k":i}
        #learners.append(lrl.LinRegLearner(**kwargs))
