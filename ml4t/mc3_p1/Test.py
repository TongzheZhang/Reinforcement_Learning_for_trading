from CART import CART
import numpy as np

np.random.seed(1)

learner = CART(max_depth=5, max_leaf_size=10)
learner.addEvidence(np.random.randint(0,10,(1000,10)), \
            np.random.random((1000)))

test_x = np.random.randint(0,10,(10))
print (test_x)

y = learner.query(test_x)

print y
