import logging

from scipy.spatial import distance

from .node import Node


class PathFinder:
    def __init__(self, game_state, player_state) -> None:
        self.gs = game_state
        self.ps = player_state

    def find_path(self, target_location):
        openlist = []
        closelist = []

        # Create starting node i.e. player's location
        starting_node = Node(self.ps.location, target_location)

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
            children = self.nearest_neighbour(current_node.position, {'a', 't'})
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

    def nearest_neighbour(self, location: tuple, search_list: set) -> list:
        x, y = location

        # Generate points of closest neighbour
        neighbours = [{(x-1, y): 'l'}, {(x+1, y): 'r'}, {(x, y-1): 'd'}, {(x, y+1): 'u'}]

        # Remove obstacle from the array and check boundry
        valid_neighbours = list()
        for neighbour in neighbours:
            for coord, action in neighbour.items():
                # Check coordinate is in bounds
                if self.gs.is_in_bounds(coord):
                    if self.gs.is_occupied(coord):
                        # TODO: avoid bomb radius
                        if self.gs.entity_at(coord) in search_list:
                            valid_neighbours.append({coord: action})
                    # Is in bounds and nothing is occupying the space
                    else:
                        valid_neighbours.append({coord: action})

        return valid_neighbours

    def find_closest_obj(self, player_location: tuple, list_of_coord: list) -> tuple:
        """Find the closest object relative to the player

        Args:
            player_location (tuple): current coordinates of the player (x,y)
            list_of_coord (list): list of tuples containing all coordinates to check

        Returns:
            tuple: closes coordinate relative to the players location
        """
        # Check if objects are avaliable on the map
        if list_of_coord:
            obj_location = dict()

            for loc in list_of_coord:
                obj_location[loc] = distance.euclidean(player_location, loc)

            return min(obj_location, key=obj_location.get)
        else:
            return ()
