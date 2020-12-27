import logging

from .helpers import Score
from .helpers import nearest_neighbour


class B1:
    def __init__(self, gs) -> None:
        self.gs = gs
        self.blocks = gs.soft_blocks + gs.ore_blocks

    @property
    def target_sites(self) -> list:
        score = []

        for block in self.blocks:
            wood_cnt = 0.0
            ore_cnt = 0.0
            is_accessible = False
            bombing_sites = []

            # Get surrounding blocks
            adjacent_blocks = nearest_neighbour(self.gs, block, {'sb', 'ob', 't', 'a'})

            # Count surrounding block type
            for adjacent_block in adjacent_blocks:
                location = list(adjacent_block.keys())[0]
                entity = self.gs.entity_at(location)
                if entity == 'sb':
                    wood_cnt += 1
                elif entity == 'ob':
                    ore_cnt += 1

                if not is_accessible and not self.gs.is_occupied(location):
                    is_accessible = True
                    # Ensure bombing sites have a safe exit
                    exit_1 = self.get_surrounding_tiles(location)
                    exit_2 = self.get_surrounding_tiles(location, radius=2)

                    if exit_1 and exit_2:
                        bombing_sites.append(location)

            if is_accessible:
                score.append(Score(block, self.score(wood_cnt, ore_cnt), bombing_sites))

        if score:
            score.sort(key=lambda s: s.score, reverse=True)
        return score

    def score(self, wood: float, ore: float) -> float:
        return wood * 0.5 + ore

    def blast_zone(self):
        blast_zone = []

        for x, y in self.gs.bombs:
            logging.info(f'Bomb at {(x,y)}')
            possible_zones = [(x, y), (x+1, y), (x+2, y), (x, y+1), (x, y+2), (x-1, y), (x-2, y), (x, y-1), (x, y-2)]

            for zone in possible_zones:
                if self.gs.is_in_bounds(zone):
                    # if self.gs.is_occupied(zone):
                    #     if self.gs.entity_at(zone) in ['a', 't', 'b']:
                    #         blast_zone.append(zone)
                    # else:
                    blast_zone.append(zone)

        return blast_zone

    def safe_zone(self, player_location, blast_zone):
        # How far out to search for a safe tile
        radius = 3
        safe_zone = []
        surrounding_tiles = []

        for r in range(1, radius+1):
            surrounding_tiles = surrounding_tiles + self.get_surrounding_tiles(player_location, r)

        for tile in surrounding_tiles:
            if tile not in blast_zone:
                safe_zone.append(tile)

        return safe_zone

    def get_surrounding_tiles(self, location, radius=1):

        # find all the surrounding tiles relative to us
        # location[0] = col index; location[1] = row index
        tile_up = (location[0], location[1]+radius)
        tile_down = (location[0], location[1]-radius)
        tile_left = (location[0]-radius, location[1])
        tile_right = (location[0]+radius, location[1])

        # combine these into a list
        all_surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

        # we'll need to remove tiles that cross the border of the map
        # start with an empty list to store our valid surrounding tiles
        valid_surrounding_tiles = []

        # loop through our tiles
        for tile in all_surrounding_tiles:
            # check if the tile is within the boundaries of the game
            if self.gs.is_in_bounds(tile):
                if self.gs.is_occupied(tile):
                    if self.gs.entity_at(tile) in ['a', 't']:
                        valid_surrounding_tiles.append(tile)
                else:
                    # if yes, then add them to our list
                    valid_surrounding_tiles.append(tile)

        return valid_surrounding_tiles
