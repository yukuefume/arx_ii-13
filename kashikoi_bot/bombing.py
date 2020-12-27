import logging
from dataclasses import dataclass


@dataclass
class Score:
    block_pos: tuple
    score: float
    b_sites: list


class Bombing:
    def __init__(self, pf, b1) -> None:
        self.pf = pf
        self.blocks = pf.gs.soft_blocks + pf.gs.ore_blocks
        self.b1 = b1

    @property
    def target_sites(self) -> list:
        score = []

        for block in self.blocks:
            wood_cnt = 0.0
            ore_cnt = 0.0
            is_accessible = False
            bombing_sites = []

            # Get surrounding blocks
            adjacent_blocks = self.pf.nearest_neighbour(block, {'sb', 'ob', 't', 'a'})

            # Count surrounding block type
            for adjacent_block in adjacent_blocks:
                location = list(adjacent_block.keys())[0]
                entity = self.pf.gs.entity_at(location)
                if entity == 'sb':
                    wood_cnt += 1
                elif entity == 'ob':
                    ore_cnt += 1

                if not is_accessible and not self.pf.gs.is_occupied(location):
                    is_accessible = True
                    # Ensure bombing sites have a safe exit
                    exit_1 = self.b1.get_surrounding_tiles(location)
                    exit_2 = self.b1.get_surrounding_tiles(location, radius=2)

                    if exit_1 and exit_2:
                        bombing_sites.append(location)

            if is_accessible:
                score.append(Score(block, self.score(wood_cnt, ore_cnt), bombing_sites))

        if score:
            score.sort(key=lambda s: s.score, reverse=True)
        return score

    def score(self, wood: float, ore: float) -> float:
        return wood * 0.5 + ore
