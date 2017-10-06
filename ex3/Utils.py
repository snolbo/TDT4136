import math
import Visuals

class Node:
    next_node_id = 0

    # processed_symbols
    OPEN = "o"
    CLOSED = "c"
    PATH = "p"
    UNVISITED = "u"

    def __init__(self):
        self.ID = Node.next_node_id   # ID of state, increment for each node to get uniqueness
        Node.next_node_id += 1
        self.g = math.inf   # cost getting to node from start
        self.h = math.inf   # estimate cost getting to goal from node
        self.f = math.inf   # f = g+h
        self.status = False # Visited: True/False
        self.parent = None  # Pointer to best parent node
        self.neighbors = []  # List of children nodes

    def get_heuristic_properties(self):
        return 0



class Cartesian2DNode(Node): # Node placed in a cartesian 2D grid
    def __init__(self, row, col, symbol,  cost=1):
        super(Cartesian2DNode, self).__init__()
        self.row = row
        self.col = col
        self.cell_type = cost  # Cost going to this cell
        self.cell_symbol = symbol  # symbol to hold terraintype of cell
        self.processed_symbol = None  # Symbol to hold how this node was processed


    def get_heuristic_properties(self):
        return [self.row, self.col]






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


class BoardParcer:
    ROAD = 1
    GRASSLAND = 5
    FOREST = 10
    MOUNTAIN = 50
    WATER = 100

    COSTDICT = {".": 1,
                "#": math.inf,
                "A": 1,
                "B": 1,
                "r": ROAD,
                "g": GRASSLAND,
                "f": FOREST,
                "m": MOUNTAIN,
                "w": WATER}

    # returns list of [row, col} of map and list of generated nodes
    @staticmethod
    def create_2dnodes_from_file(txtfilename):
        file_object = open(txtfilename, "r")
        generated_nodes = []
        rows = 0
        cols = 0
        start_node = []
        goal_node = []
        # Create the nodes
        index = 0
        for line in file_object:
            cols = 0
            for symbol in line:
                if symbol in BoardParcer.COSTDICT:
                    generated_nodes.append(BoardParcer.create_2dnode_from_symbol(symbol, rows, cols))
                    if symbol == "A":
                        start_node = generated_nodes[index]
                    if symbol == "B":
                        goal_node = generated_nodes[index]
                    cols += 1
                    index += 1
            rows += 1

        Visuals.ImageCreator.create_image(txtfilename.replace(".txt", ".bmp"), cols, rows)
        coords = []
        cell_symbols = []
        # Connect the nodes with neighbors
        for i in range(0, rows):
            for j in range(0, cols):
                ## Commented out statements create 8 - neighborhood
                coords.append((j,i))
                cell_symbols.append(generated_nodes[i*cols + j].cell_symbol)
                # if j != 0 and i != 0:
                #     generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i-1)*cols + (j-1)])
                if i != 0:
                    generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i-1)*cols + (j)])
                # if j != cols-1 and i != 0:
                #     generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i-1)*cols + (j+1)])

                if j != 0:
                    generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i)*cols + (j-1)])
                if j != cols-1:
                    generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i)*cols + (j+1)])

                # if j != 0 and i != rows-1:
                #     generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i+1)*cols + (j-1)])
                if i != rows-1:
                    generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i+1)*cols + (j)])
                # if j != cols-1 and i != rows-1:
                #     generated_nodes[i*cols + j].neighbors.append(generated_nodes[(i+1)*cols + (j+1)])
        Visuals.ImageCreator.draw_pixels_on_image(coords, cell_symbols)
        file_object.close()
        return [[rows, cols], start_node, goal_node, generated_nodes]

    # Return 2d node with cost given by symbol
    @staticmethod
    def create_2dnode_from_symbol(symbol, row, col):
        cost = BoardParcer.COSTDICT[symbol]
        return Cartesian2DNode(row, col, symbol, cost)

