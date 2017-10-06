import math
import Utils
import PIL
import Visuals


class AStarSearch:
    UNVISITED = 0
    OPEN = 1
    CLOSED = 2

    def __init__(self, all_nodes,  start_node, goal_node, heuristic_property_evaluator=None):
        self.open = []    # List holding the horizon of the search space sorted by lowest f value gained from expansion of its parent
        self.closed = []  # List holding visited nodes that have have had  its children expanded
        self.start_node_ = start_node
        self.goal_node_ = goal_node
        self.heuristic_property_evaluator_ = heuristic_property_evaluator

        # self.search_states = {} # Hash table to hold all states generated, with state ID as hash key
        # for node in all_nodes:
        #     self.search_states[node.ID] = AStarSearch.UNVISITED

        start_node.g = 0
        if heuristic_property_evaluator is not None:
            start_node.h = self.calculate_heuristic(start_node)
        start_node.f = start_node.g + start_node.h
        self.insert_node_to_open(start_node)
        return

    def start_search(self):
        while self.open: # While there are still elements in open list
            # Find next node from open
            node = self.get_next_node()
            # See if node is goal node, perform complete-routine if true
            if node == self.goal_node_:
                print("FOUND GOAL NODE!") # Complete-routine
                return node

            # For all successors of node: calculate heuristic, add to open set if not there, update if already in closed or open set
            for neigh in node.neighbors:
                # Calculate g h and f for successor based on node.g and cost of going there
                g = node.g + neigh.cell_type
                h = self.calculate_heuristic(neigh)
                f = g + h
                if f == math.inf:  # Cant go here, there is a wall or infinitely large cost going here. Discard this option
                    continue
                # Handles how updates are made
                self.perform_updates(node, neigh, g, h, f)
            # Remove node from OPEN, add node to CLOSED, mark node ID as closed
            self.process_finished_node(node)
        # GOAL node was not found
        print("GOAL NODE NOT FOUND")
        return

    # Update parenthood and heuristic if neigh in open or closed and f is smaller than prev. otherwise add to open set
    def perform_updates(self, node, neigh, g, h, f):
        # in_open = self.search_states[neigh.ID] == AStarSearch.OPEN
        in_open = neigh.processed_symbol == Utils.Node.OPEN
        # in_closed = self.search_states[neigh.ID] == AStarSearch.CLOSED
        in_closed = neigh.processed_symbol == Utils.Node.CLOSED

        if in_open or in_closed:  # If neigh in open or closed and f < this node's calculated f
            if f < neigh.f:
                # Update heuristics
                neigh.g = g
                neigh.h = h
                neigh.f = f
                # Set new parent, as this parent gave better heuristic
                neigh.parent = node
                print("Found better parent for  " + str(neigh.ID) + " Parent set to " + str(node.ID))
                if in_closed:  # If successor in CLOSED
                    # recursively update heuristic for all children of neigh, since they now get better heuristic
                    print(str(neigh.ID) + " updating parent")
                    self.update_children_heuristics(neigh)
            # ELSE do nothing
        else:  # If none of the above: add neigh to OPEN
            neigh.g = g
            neigh.h = h
            neigh.f = g + h
            neigh.parent = node
            self.insert_node_to_open(neigh)
        return

    # Called when a closed node has received a new parent by result of better heuristic estimate. Updates heuristic of all
    # neighbors that the node is the best parent of, recursively
    def update_children_heuristics(self, source_node):
        # print("Recursion from id: " + str(source_node.ID))
        for neigh in source_node.neighbors:
            if source_node == neigh.parent:  # If neigh is in open or closed
                # Update heuristics
                neigh.g = source_node.g + neigh.cell_type
                neigh.f = neigh.g + neigh.h
                # Update children heuristics
                self.update_children_heuristics(neigh)  # Recursive call
        return

    # Inserts a node into the open set based on heuristic value. Lowest value is first in list.
    def insert_node_to_open(self, node):
        # Place node into Open based on its heuristic. best heuristic gets placed first
        # self.search_states[neigh.ID] = AStarSearch.OPEN  # mark node ID as open
        node.processed_symbol = Utils.Node.OPEN
        for i in range(0, len(self.open)):
            if node.f < self.open[i].f:
                self.open.insert(i, node)
                return
        self.open.append(node)  # If worst heuristic, append to end of OPEN
        return

    # Simple ruitine for when a node from open set  has been processed to completion
    def process_finished_node(self, node):
        self.open.remove(node)
        self.closed.append(node)
        # self.search_states[node.ID] = AStarSearch.CLOSED
        node.processed_symbol = Utils.Node.CLOSED
        return




    # Used to get next node from open set. Currently implementation results in breath first. A* if inserting nodes
    # Into open set happens by inserting by heuristic value
    def get_next_node(self):
        return self.open[0]



    # Calculate the heuristic of the node in regards to its properties and the properties of the goal node
    def calculate_heuristic(self, source_node):
        node_properties = source_node.get_heuristic_properties()
        goal_node_properties = self.goal_node_.get_heuristic_properties()
        return self.heuristic_property_evaluator_(node_properties, goal_node_properties, len(node_properties))





class BreathFirstSearch(AStarSearch):
    def __init__(self, all_nodes, start_node, goal_node, heuristic_property_evaluator=None):
        super(BreathFirstSearch, self).__init__(all_nodes, start_node, goal_node, None)

    def start_search(self):
        while self.open:  # While there are still elements in open list
            # Find next node from open
            node = self.get_next_node()
            # See if node is goal node, perform complete-routine if true
            if node == self.goal_node_:
                print("FOUND GOAL NODE!") # Complete-routine
                return node

            # For all successors of node: calculate heuristic, add to open set if not there, update if already in closed or open set
            for neigh in node.neighbors:
                # in_open = self.search_states[neigh.ID] == AStarSearch.OPEN
                in_open = neigh.processed_symbol == Utils.Node.OPEN

                # in_closed = self.search_states[neigh.ID] == AStarSearch.CLOSED
                in_closed = neigh.processed_symbol == Utils.Node.CLOSED

                if not in_open and not in_closed: # Only want to consider this node if not processed already
                    # Calculate new g
                    g = node.g + neigh.cell_type #  Does not matter what we put here, as long at its not inf
                    if g == math.inf:  # Cant go here, there is a wall or infinitely large cost going here. Discard this option
                        continue
                    # Add cost to new node. Add and tag it as open
                    neigh.g = g
                    neigh.parent = node
                    # self.search_states[neigh.ID] = AStarSearch.OPEN  # mark node ID as open
                    neigh.processed_symbol = Utils.Node.OPEN
                    self.open.append(neigh) # Now we simply place the node in back of list. Since we get nodes from front, this become breath first
            # Remove node from OPEN, add node to CLOSED, mark node ID as closed
            self.process_finished_node(node)
        # GOAL node was not found
        print("GOAL NODE NOT FOUND")
        return


class Dijkstra(AStarSearch):
    def __init__(self, all_nodes, start_node, goal_node, heuristic_property_evaluator=None):
        super(Dijkstra, self).__init__(all_nodes, start_node, goal_node, None)

    def start_search(self):
        while self.open:  # While there are still elements in open list
            # Find next node from open
            node = self.get_next_node()
            # See if node is goal node, perform complete-routine if true
            if node == self.goal_node_:
                print("FOUND GOAL NODE!") # Complete-routine
                return node

            # For all successors of node: calculate heuristic, add to open set if not there, update if already in closed or open set
            for neigh in node.neighbors:
                # in_open = self.search_states[neigh.ID] == AStarSearch.OPEN
                in_open = neigh.processed_symbol == Utils.Node.OPEN

                # in_closed = self.search_states[neigh.ID] == AStarSearch.CLOSED
                in_closed = neigh.processed_symbol == Utils.Node.CLOSED

                if not in_open and not in_closed: # Only want to consider this node if not processed already
                    # Calculate new g
                    g = node.g + neigh.cell_type
                    f = g  # Our heuristic is now only the cost going to next node, and we pick the one with lowest cost
                    if f == math.inf:  # Cant go here, there is a wall or infinitely large cost going here. Discard this option
                        continue
                    # Add cost to new node. Add and tag it as open
                    neigh.g = g
                    neigh.f = f
                    neigh.parent = node
                    self.insert_node_to_open(neigh) # now we just use our insert, which places the node such that we always pick cheapest available option as next
            self.process_finished_node(node)
        # GOAL node was not found
        print("GOAL NODE NOT FOUND")
        return



