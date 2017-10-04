import math
import Utils


class BestFirstSearch:
    UNVISITED = 0
    OPEN = 1
    CLOSED = 2

    def __init__(self, start_node, goal_node, heuristic_property_evaluator=None):
        self.open_ = []    # List holding the horizon of the search space sorted by lowest f value gained from expansion of its parent
        self.closed_ = []  # List holding visited nodes that have have had  its children expanded
        self.start_node_ = start_node
        self.goal_node_ = goal_node
        self.heuristic_property_evaluator_ = heuristic_property_evaluator
        self.search_states = {} # Hash table to hold all states generated, with state ID as hash key
        return

    def start_search(self):

        while self.open_: # While there are still elements in open list
            # Find next node from open
            node = self.get_next_node()

            # See if node is goal node, perform complete-routine if true
            if node == self.goal_node_:
                print("FOUND GOAL NODE!")
                return

            # For all successors of node
            for succ in node.neighbor:
                # Calculate g h and f for successor based on node.g and cost(node, successor)
                g = node.g + node.costs[node.children.index(succ)]
                h = self.heuristic_property_evaluator_(succ, self.goal_node_)
                f = f + h

                in_open = self.search_states[succ.ID] == BestFirstSearch.OPEN
                in_closed = self.search_states[succ.ID] == BestFirstSearch.CLOSED

                # If successor already in OPEN or in CLOSED
                    # if f_new < f_old. Update heuristic of successor in OPEN
                    # update best parent of successor to node
                if (in_open or in_closed) and f < succ.f:
                    succ.g = g
                    succ.h = h
                    succ.f = g + h
                    succ.parent = node
                    if in_closed:  # If successor in CLOSED
                        # recursively update heuristic for all children of succsessor
                        self.update_neighbor_heuristics(succ)
                else: # If none of the above: add successor to OPEN
                    self.insert_node_to_open(succ)

            # Remove node from OPEN, add node to CLOSED
            self.open_.remove(node)
            self.closed_.append(node)


    def update_neighbor_heuristics(self, node):
        for succ in node.neighbor:
            if self.search_states[succ.ID] != BestFirstSearch.UNVISITED:  # If succ is in open or closed
                succ.g = node.g + node.costs[node.children.index(succ)]
                succ.f = succ.g + succ.h
                self.update_neighbor_heuristics(succ)  # Recursive call
        return


    def get_next_node(self):
        return self.open_[0]  # This in reality is breath first

    def insert_node_to_open(self, node):
        self.open_.append(node)  # Pushes node to last element in open
        return


    # Calculate the heuristic of the node in regards to its properties and the properties of the goal node
    def calculate_heuristic(self, node):
        node_properties = node.get_heuristic_properties()
        goal_node_properties = self.goal_node_.get_heuristic_properties()
        len1 = len(node_properties)
        len2 = len(goal_node_properties)
        if len1 != len2:
            print("YOU FUCKED UP MATE! len heuristic_properties: " + str(len1) + " len goal_node_properties: " + str(len2))
            return
        return self.heuristic_property_evaluator_(node_properties, goal_node_properties, len1)


class DepthFirstSearch(BestFirstSearch):
    def __init__(self, start_node, goal_node):
        super(DepthFirstSearch, self).__init__(start_node, goal_node)
        return

    def get_next_node(self):
        return self.open_[-1]  # Returning last element pushed to OPEN


class BreathFirstSearch(BestFirstSearch):
    def __init__(self, start_node, goal_node):
        super(BreathFirstSearch, self).__init__(start_node, goal_node)
        return


class AStartSearch(BestFirstSearch):
    def __init__(self, start_node, goal_node, heuristic_property_evaluator):
        super(AStartSearch, self).__init__(start_node, goal_node, heuristic_property_evaluator)
        return

    def start_search(self):
        return

    def insert_node_to_open(self, node):
        # Place node into Open based on its heuristic. best heuristic gets placed first
        for i in range(0, len(self.open_)):
            if node.f < self.open_[i]:
                self.open_.insert(i, node)
                return
        self.open_.append(node)  # If worst heuristic, append to end of OPEN
        return



print("Debugging print")
print(str(Utils.HeuristicCalculator.manhattan_property_evaluator([0,0], [3,4], 2)))
print(str(Utils.HeuristicCalculator.euclidean_property_evaluator([0,0], [3,4], 2)))


list = [1, 2, 3,4]
# while list:
#     print(str(list.pop()))

ob1 = {}
ob2 = {}

n = Utils.Cartesian2DNode()
n.parent = "ARE custom classes are mutable objects??? "


ob1[0] = n
ob2[0] = n

print(str(ob1[0].parent))
print(str(ob2[0].parent))

n.parent = "custom classes are mutable objects :) "

print(str(ob1[0].parent))
print(str(ob2[0].parent))



