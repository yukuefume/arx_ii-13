from dataclasses import dataclass

from scipy.spatial import distance


class Node:
    def __init__(self, position: tuple, target_location: tuple, action: str = '', parent: 'Node' = None) -> None:
        self.position = position
        self.parent = parent
        self.action = action

        if parent is not None:
            self._h = distance.cityblock(position, target_location)
            self._g = self.parent.g + 1
            self._f = self._h + self._g
        else:
            self._h = 0
            self._g = 0
            self._f = 0

    @property
    def f(self) -> int:
        return self._f

    @property
    def g(self) -> int:
        return self._g

    @property
    def h(self) -> int:
        return self._h

    def path(self) -> list:
        path = []
        current_node = self
        while current_node:
            path.append(current_node)
            current_node = current_node.parent

        path.pop()
        return path

    @property
    def show_path(self) -> list:
        path = self.path()
        path.reverse()
        return [node.position for node in path]

    def __hash__(self) -> int:
        return hash((self.position, self.action, self.f))

    def __eq__(self, o: object) -> bool:
        return (self.position == o.position and
                self.action == o.action and
                self.h == o.h and
                self.g == o.g and
                self.f == o.f)

    def __str__(self) -> str:
        return (f"Position: {self.position}, "
                f"Parent: { self.parent.position if self.parent else 'None' }, "
                f"f: {self.f}, "
                f"g: {self.g}, "
                f"h: {self.h}")


@dataclass
class Score:
    block_pos: tuple
    score: float
    b_sites: list


def find_closest_obj(player_location: tuple, list_of_coord: list) -> tuple:
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


def nearest_neighbour(gs, location: tuple, search_list: set) -> list:
    x, y = location

    # Generate points of closest neighbour
    neighbours = [{(x-1, y): 'l'}, {(x+1, y): 'r'}, {(x, y-1): 'd'}, {(x, y+1): 'u'}]

    # Remove obstacle from the array and check boundry
    valid_neighbours = list()
    for neighbour in neighbours:
        for coord, action in neighbour.items():
            # Check coordinate is in bounds
            if gs.is_in_bounds(coord):
                if gs.is_occupied(coord):
                    # TODO: avoid bomb radius
                    if gs.entity_at(coord) in search_list:
                        valid_neighbours.append({coord: action})
                # Is in bounds and nothing is occupying the space
                else:
                    valid_neighbours.append({coord: action})

    return valid_neighbours
