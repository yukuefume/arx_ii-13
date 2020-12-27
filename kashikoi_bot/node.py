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
