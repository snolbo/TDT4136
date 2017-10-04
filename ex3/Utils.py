import math


class Node:
    def __init__(self):
        self.ID = None   # ID of state
        self.g = math.inf   # cost getting to node from start
        self.h = math.inf   # estimate cost getting to goal from node
        self.f = math.inf   # f = g+h
        self.status = False # Visited: True/False
        self.parent = None  # Pointer to best parent node
        self.neighbor =  [] # List of children nodes
        self.costs = []     # Cost of going to children nodes

    def get_heuristic_properties(self):
        return 0



class Cartesian2DNode(Node): # Node placed in a cartesian 2D grid
    def __init__(self):
        super(Cartesian2DNode, self).__init__()
        self.x = 0
        self.y = 0

    def get_heuristic_properties(self):
        return [self.x, self.y]






class HeuristicCalculator:
    @staticmethod
    def euclidean_property_evaluator(props1, props2, properties_len):
        heuristic = 0
        for i in range(0, properties_len):
            heuristic += math.pow(props1[i] - props2[i], 2)
        heuristic = math.sqrt(heuristic)
        return heuristic

    @staticmethod
    def manhattan_property_evaluator(props1, props2, properties_len):
        heuristic = 0
        for i in range(0, properties_len):
            heuristic += math.fabs(props1[i] - props2[i])
        return heuristic

