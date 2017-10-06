import Algorithms
import Visuals
import Utils

bp = Utils.BoardParcer()

for i in range(1,3):
    for j in range(1,5):
        [dims, start_node, goal_node, all_nodes] = bp.create_2dnodes_from_file("./boards/board-" + str(i) + "-" + str(j) + ".txt")
        rows = dims[0]
        cols = dims[1]
        print("dims: " + str(rows) + "  " + str(cols))
        print("start node ID: " + str(start_node.ID))
        print("goal node ID: " + str(goal_node.ID))

        search = Algorithms.AStarSearch(all_nodes, start_node, goal_node, Utils.HeuristicCalculator.manhattan_property_evaluator)
        end_node = search.start_search()

        print("Found correct goal node: " + str(end_node.ID == goal_node.ID), end="\n\n")
        parent = end_node
        while parent is not None:
            parent.processed_symbol = Utils.Node.PATH
            parent = parent.parent

        node_coords = []
        node_symbols = []

        for node in all_nodes:
            if node.processed_symbol is not None:
                node_coords.append((node.col, node.row))
                node_symbols.append(node.processed_symbol)

        Visuals.ImageCreator.draw_search_results_on_image(node_coords, node_symbols)
        
