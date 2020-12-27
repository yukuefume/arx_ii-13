import logging

from .helpers import Node
from .helpers import nearest_neighbour


def find_path(player_location, target_location, game_state):
    openlist = []
    closelist = []

    # Create starting node i.e. player's location
    starting_node = Node(player_location, target_location)

    openlist.append(starting_node)

    # Continue searching while openlist is populated
    logging.debug('--- A* Start ---')
    while len(openlist) > 0:
        logging.debug(f'Iterating open list node: {[ o.position for o in openlist ]}')
        # Find the lowest f score in the openlist
        current_node = openlist[0]
        current_index = 0
        for index, node in enumerate(openlist):
            logging.debug(str(node))
            if node.f < current_node.f:
                current_node = node
                current_index = index
        logging.debug(f'Current node is: {str(current_node)}')

        # Move current node into closelist
        openlist.pop(current_index)
        closelist.append(current_node)

        # Path found
        if current_node.position == target_location:
            if current_node == starting_node:
                return [current_node]
            else:
                return current_node.path()

        # Get all nearest squares of current node
        children = nearest_neighbour(game_state, current_node.position, {'a', 't'})
        logging.debug(f'Children: {children}')
        for child in children:
            for coord, action in child.items():
                # Check if child is in closelist
                if coord in [node.position for node in closelist]:
                    continue

                child_node = Node(coord, target_location, action, current_node)

                # Check if child is already in openlist and has a higher g value that the existing node
                for open_node in openlist:
                    if child_node == open_node and child_node.g > open_node.g:
                        continue

                openlist.append(child_node)
        logging.debug(f'Close list: {[ c.position for c in closelist ]}')

    logging.info('Cannot find sutible path')
    logging.debug('--- A* End ---')
    return []
