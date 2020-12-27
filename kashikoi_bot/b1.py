import logging


class B1:
    def __init__(self, game_state) -> None:
        self.gs = game_state

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
