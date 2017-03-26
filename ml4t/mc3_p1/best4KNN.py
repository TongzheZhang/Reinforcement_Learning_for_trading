import numpy as np
import csv


if __name__=="__main__":
    a = np.empty((1000,3))
    noise = np.random.normal(0,1,size = (1000))
    #print a.shape
    #print noise.shape
    #print a[:,2].shape
    m = np.random.randint(0,10,1000)
    n = np.random.randint(0,10,1000)
    a[:,0] = m
    a[:,1] = n
    a[:,2] = a[:,0]**5 + a[:,1]**4
    a[:,2] = a[:,2] + noise
   
    with open('best4KNN.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(a)
