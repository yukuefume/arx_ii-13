'''
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO: 
ARX II-13 is an older variant of the ARX line of androids.
It was once used by the world's elite military forces under a top secret program codenamed 'Genesis' as a time travelling
assasin. It now has been re-purpose to undergo a dangerous mining program in Dungeons and Data Structures.

It primarily focuses on mining high value minerals such as Ore, or valuable wood. To keep it safe from the environment it
has been fitted with the B1 chip which is its bomb avoidance system.

As it has been seriously damaged in the battlefield, it's self-defence mechanism is no longer functional and therefore
only injures or kills it's opponents by chance, while its primary focus is on mining and survival.
'''

import random
import logging


class Agent:
    def __init__(self):
        self.planned_actions = []
        self.evasive_actions = []
        logging.getLogger().setLevel(logging.INFO)

    def next_move(self, game_state, player_state):
        action = ''
        # Create path finder object each turn as game_state or player_state may change
        pf = PathFinder(game_state, player_state)
        b1 = B1(game_state)

        if len(game_state.bombs) > 0:
            if not self.evasive_actions:
                blast_zone = b1.blast_zone()
                logging.info(f'Player at {player_state.location}')
                logging.info(f'Blast zone: {blast_zone}')
                if player_state.location in blast_zone:
                    logging.info(f'Inside danger zone: {blast_zone}')
                    safe_zones = b1.safe_zone(player_state.location, blast_zone)
                    logging.info(f'Safe zones found {safe_zones}')
                    for safe_zone in safe_zones:
                        path = pf.find_path(safe_zone)
                        if path:
                            logging.info(f'Moving to safe zone: {safe_zone}')
                            self.evasive_actions = ['', '']
                            for p in path:
                                self.evasive_actions.append(p.action)
                                self.planned_actions = []
                            break
                # If player is near blast zone wait
                elif any(pos in blast_zone for pos in b1.get_surrounding_tiles(player_state.location)):
                    self.evasive_actions = ['', '']

        if self.evasive_actions:
            action = self.evasive_actions.pop()
        # If we have a plan - follow it
        elif self.planned_actions:
            action = self.planned_actions.pop()
        # We have bombs plant em'
        elif player_state.ammo > 0:
            # Get possible bomb sites
            bombing = Bombing(pf, b1)
            ranked_target_sites = bombing.target_sites
            logging.info(f'Targets: {ranked_target_sites}')
            # Find a viable bombing spot
            path = []
            for target_site in ranked_target_sites:
                for site in target_site.b_sites:
                    path = pf.find_path(site)
                    if path:
                        logging.info(f'Planting bomb at {site}')
                        logging.info(f'Path to bomb site {path[0].show_path}')
                        break
                if path:
                    break
            if path:
                self.planned_actions.append('p')
                for p in path:
                    self.planned_actions.append(p.action)
        else:
            target = game_state.treasure + game_state.ammo
            closest_target = pf.find_closest_obj(player_state.location, target)

            if target:
                random_target = random.choice(target)
                entity = game_state.entity_at(closest_target)
                if entity == 't':
                    entity = 'treasure'
                elif entity == 'a':
                    entity = 'ammo'
                logging.info(f'Picking up {entity}')
                logging.info(f'Finding path for {closest_target}')
                path = pf.find_path(closest_target)
                if path:
                    logging.info(f'Path found (closest): {path[0].show_path}')
                    for p in path:
                        self.planned_actions.append(p.action)
                else:
                    path = pf.find_path(random_target)
                    logging.info(f'Path found (random): {path[0].show_path}')
                    for p in path:
                        self.planned_actions.append(p.action)
        return action
