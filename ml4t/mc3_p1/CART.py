from Node import Node

class CART ():
    def __init__(self, max_depth, max_leaf_size):
        self.max_depth = max_depth
        self.max_leaf_size = max_leaf_size

def addEvidence(self, Xtrain, Ytrain):
    self.tree = self.addNode(Xtrain ,Ytrain ,0)
    self.draw_tree()

def addNode(self, X, y, depth):
    node = Node ()

    if (depth >= self.max_depth) or (X.shape[0] <= self.max_leaf_size):
        node.y = y.mean()
        return node

    best_unevenness = float('Inf')

    for factor in range(0,X.shape[1]):
        sorted = X[:,factor].argsort()
        split_idx = int(X.shape[0] / 2)

        while split_idx > 0 and (X[sorted][split_idx ,factor] == \
                                    X[sorted][split_idx -1,factor]):
            split_idx -= 1

    unevenness = abs(split_idx - (X.shape[0] - split_idx))
    if unevenness < best_unevenness:
        best_unevenness = unevenness
        best_factor = factor
        best_sorted = sorted
        best_split_idx = split_idx
        best_split_val = X[sorted][split_idx ,factor]

    node.split_factor = best_factor
    node.split_val = best_split_val

    node.left = self.addNode(X[best_sorted][:best_split_idx], \
                                y[best_sorted][:best_split_idx], depth +1)

    node.right = self.addNode(X[best_sorted][best_split_idx:], \
                                y[best_sorted][best_split_idx:], depth +1)

    return node

    def query(self, Xtest):
        node = self.tree

        while node.y == None:
            if Xtest[node.split_factor] < node.split_val:
                node = node.left
            else:
                node = node.right
        return node.y



    def draw_tree(self):
        node = self.tree
        self.viz_tree_node(node ,0)

    def viz_tree_node(self, node, depth):
        print ' ' * (depth * 4),
        if node.y != None:
            print '( y =', node.y, ')'
        return
    print '(', node.split_factor , ',', node.split_val , ')'
    if node.left:
        self.viz_tree_node(node.left,depth+1)
    if node.right:
        self.viz_tree_node(node.right,depth+1)
