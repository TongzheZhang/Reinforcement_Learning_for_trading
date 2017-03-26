import numpy as np

class Node ():
    def __init__(self):

        self.split_factor = -1
        self.split_val = None
        self.left = None
        self.right = None
        self.y = None
