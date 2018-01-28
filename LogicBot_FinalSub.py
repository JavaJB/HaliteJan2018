import hlt
import logging
from collections import OrderedDict
# GAME START
game = hlt.Game("JbBot-v3")
logging.info("Starting JbBot-v3!")

# useful for getting a planet (key) from it's distance (value)
def key_by_value(dictionary, value):
    for k,v in dictionary.items():
        if v[0] == value:
            return k
    return -99

def target_closest_enmey_ships(Ship myship, List enemy_ships, List command_queue):
    target_ship = closest_enemy_ships[0]
    navigate_command = ship.navigate(
        ship.closest_point_to(target_ship),
        game_map,
        speed = int(hlt.constants.MAX_SPEED),
        ignore_ships = False)
    if navigate_command:
        command_queue.append(navigate_command)

ship_plans = {}


while True:
    # TURN START
    game_map = game.update_map()
    command_queue = []

    my_ships = game_map.get_me().all_ships()
    all_ships = game_map._all_ships()
    enemy_ships = [ship for ship in game_map._all_ships() if ship not in my_ships]

    my_ship_count = len(my_ships)
    enemy_ship_count = len(enemy_ships)
    all_ship_count = len(all_ships)

    my_id = game_map.get_me().id

    empty_planet_sizes = {}
    my_planet_sizes = {}
    enemy_planet_sizes = {}

    # for each turn categorize the planets by radius
    for p in game_map.all_planets():
        radius = p.radius
        if not p.is_owned(): # empty planet
            empty_planet_sizes[radius] = p
        elif p.owner.id == game_map.get_me().id: # one of my planets
            my_planet_sizes[radius] = p
        elif p.owner.id != game_map.get_me().id: # enemy planet, possibly change to just else statement
            enemy_planet_sizes[radius] = p

    my_planets_count = len(my_planet_sizes)
    empty_planets_count = len(empty_planet_sizes)
    enemy_planets_count = len(enemy_planet_sizes)

    empty_planet_keys = sorted([k for k in empty_planet_sizes])[::-1]
    my_planet_keys = sorted([k for k in my_planet_sizes])[::-1]
    enemy_planet_keys= sorted([k for k in enemy_planet_sizes])[::-1]

    for ship in team_ships:
        try:
            if(ship.docking_status() == ship.DockingStatus.UNDOCKED):
                continue
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

            closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]
            closest_empty_planet_distances = [distance for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

            closest_my_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned() and (entities_by_distance[distance][0].owner.id == game_map.get_me().id)]
            closest_my_planets_distances = [distance for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned() and (entities_by_distance[distance][0].owner.id == game_map.get_me().id)]

            closest_enemy_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0] not in closest_my_planets and entities_by_distance[distance][0] not in closest_empty_planets]
            closest_enemy_planets_distances = [distance for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0] not in closest_my_planets and entities_by_distance[distance][0] not in closest_empty_planets]

            closest_my_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] in my_ships]
            closest_my_ships_distances = [distance for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] in my_ships]

            closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]
            closest_enemy_ships_distances = [distance for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]

            largest_empty_planet_distances = []
            largest_my_planet_distances = []
            largest_enemy_planet_distances = []



            if(len(my_planets_count) < 1): # no planets, game start condition, note very few ships in this case
                if team_ships.index(ship) == 0: # 1st ship
                    target_planet = closest_empty_planets[0]
                    if ship.can_dock(target_planet):
                        command_queue.append(ship.dock(target_planet))
                    else:
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships = False)
                        if navigate_command:
                            command_queue.append(navigate_command)
                elif team_ships.index(ship) == 1:
                    target_planet = closest_empty_planets[0]
                    if ship.can_dock(target_planet):
                        command_queue.append(ship.dock(target_planet))
                    else:
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships = False)
                        if navigate_command:
                            command_queue.append(navigate_command)
                else: # team_ships.index(ship) == 2
                    target_planet = closest_empty_planets[1]
                    if ship.can_dock(target_planet):
                        command_queue.append(ship.dock(target_planet))
                    else:
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships = False)
                        if navigate_command:
                            command_queue.append(navigate_command)
            elif len(my_planets_count) <= 3 and len(my_planets_count) >= 1: # low planet conditions
                # there are empty planets on the game board
                if len(empty_planets) > 0:
                    if closest_planets[0] is closest_friendly_planets[0]: # closest planet is mine
                        target_planet = closest_friendly_planets[0] # target said closest planet
                        if len(target_planet.all_docked_ships()) < 2 or (len(target_planet.all_docked_ships()) < (target_planet.num_docking_spots - 1)): # target planet is under-docked
                            if ship.can_dock(target_planet):    # dock if we can
                                command_queue.append(ship.dock(target_planet))
                            else: # navigate to the planet otherwise
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships = False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                        elif closest_planets[1] is closest_empty_planets[0]: # planet had enough docked ships, next closest is empty, go settle
                            target_planet = closest_empty_planets[0]
                            if ship.can_dock(target_planet):    # dock if we can
                                command_queue.append(ship.dock(target_planet))
                            else:
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships = False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                        elif closest_planets[1] is closest_friendly_planets[1]: # next closest is mine, dock check
                            target_planet = closest_planets[1]
                            # dock check my 2nd closest planet
                            if len(target_planet.all_docked_ships()) < 2 or (len(target_planet.all_docked_ships()) < (target_planet.num_docking_spots - 1)):
                                if ship.can_dock(target_planet):    # dock if we can
                                    command_queue.append(ship.dock(target_planet))
                                else: # navigate to the planet otherwise
                                    navigate_command = ship.navigate(
                                        ship.closest_point_to(target_planet),
                                        game_map,
                                        speed = int(hlt.constants.MAX_SPEED),
                                        ignore_ships = False)
                                    if navigate_command:
                                        command_queue.append(navigate_command)
                            elif : #empty closer than enemy
                            else: # default, attack ships. eventually go mess with enemies larger planets
                        else: # default, next closest planet was not mine or empty (enemy). eventually target larger enemy planets
                            target_ship = closest_enemy_ships[0]
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships = False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                    elif not closest_planets[0].is_owned(): # closest planet is unowned
                        target_planet = closest_planets[0]
                        if ship.can_dock(target_planet):    # dock if we can
                            command_queue.append(ship.dock(target_planet))
                        else: # navigate to the planet otherwise
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_planet),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships = False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                    else: # closest planet is enemy planet
                        #target_planet = closest_planets[0]
                        target_ship = closest_enemy_ships[0] # target_planet.all_docked_ships()[0] # go attack a docked enemy ship
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships = False)
                        if navigate_command:
                                command_queue.append(navigate_command)
                else: # there are no empty planets on the game board #FUCKED
                    if closest_planets[0].owner is my_id: # closest planet it mine
                        if closest_planets[0].all_docked_ships() < closest_planets[0].num_docking_spots: # not fully docked
                            target_planet = closest_planets[0]
                            if ship.can_dock(target_planet):    # dock if we can
                                command_queue.append(ship.dock(target_planet))
                            else: # navigate to the planet otherwise
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships = False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                        else : # attack nearest docked enemy ship
                            target_planet = closest_enemy_planets[0]
                            target_ship = target_planet.all_docked_ships()[0]
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships = False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                    else: # closest planet is enemy planet, attack it's docked ships
                        target_planet = closest_enemy_planets[0]
                        target_ship = target_planet.all_docked_ships()[0]
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships = False)
                        if navigate_command:
                            command_queue.append(navigate_command)
            else: # if len(my_planets) >= 4: # 4 or more my planets
                if len(empty_planets) > 0:
                    if closest_planets[0] is closest_friendly_planets[0]:  # if closest planet is mine
                        target_planet = closest_planets[0]
                        # if that planet is below dock threshold
                        if len(target_planet.all_docked_ships()) <= target_planet.num_docking_spots - 1:
                            # dock with it
                            if ship.can_dock(target_planet):
                                command_queue.append(ship.dock(target_planet))
                            else:
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                        elif len(closest_enemy_planets) > 0 and (closest_planets[1] is closest_enemy_planets[0]): # the 2nd closest planet is an enemy planet, attack w/o a dock check
                            target_ship = closest_enemy_ships[0] # attack w/o a dock check
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                        elif closest_planets[1] is closest_friendly_planets[1]: # the 2nd closest planet is mine, attack after DC-ing it
                            target_planet = closest_planets[0]
                            # planet is below dock threshold
                            if len(target_planet.all_docked_ships()) < target_planet.num_docking_spots: # <= (dock_threshold * target_planet.num_docking_spots):
                                # dock at the planet
                                if ship.can_dock(target_planet):
                                    command_queue.append(ship.dock(target_planet))
                                else:
                                    navigate_command = ship.navigate(
                                        ship.closest_point_to(target_planet),
                                        game_map,
                                        speed = int(hlt.constants.MAX_SPEED),
                                        ignore_ships=False)
                                    if navigate_command:
                                        command_queue.append(navigate_command)
                            elif len(closest_planets[1].all_docked_ships()) < target_planet.num_docking_spots: # second closest isn't fully docked
                                target_planet = closest_planets[1]
                                if ship.can_dock(target_planet):
                                    command_queue.append(ship.dock(target_planet))
                                else:
                                    navigate_command = ship.navigate(
                                        ship.closest_point_to(target_planet),
                                        game_map,
                                        speed = int(hlt.constants.MAX_SPEED),
                                        ignore_ships=False)
                                    if navigate_command:
                                        command_queue.append(navigate_command)
                            elif closest_planets[2] in enemy_planets: # go attack if there isn't a close by empty
                                target_ship = closest_enemy_ships[0]
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_ship),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                            elif len(closest_empty_planets) > 0: # close by empty, go settle NEED TO EDIT TO PREVENT CONSTANT SETTLING IN MID TO LATE GAME
                                target_planet = closest_empty_planets[0]
                                if ship.can_dock(target_planet):
                                    command_queue.append(ship.dock(target_planet))
                                else:
                                    navigate_command = ship.navigate(
                                        ship.closest_point_to(target_planet),
                                        game_map,
                                        speed = int(hlt.constants.MAX_SPEED),
                                        ignore_ships=False)
                                    if navigate_command:
                                        command_queue.append(navigate_command)
                            elif len(closest_enemy_ships) > 0:
                                target_ship = closest_enemy_ships[0]
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_ship),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                            else:
                                continue
                        else: # the 2nd closest planet is empty
                            target_planet = closest_empty_planets[0]
                            if ship.can_dock(target_planet):
                                command_queue.append(ship.dock(target_planet))
                            else:
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                    elif not closest_planets[0].is_owned(): # closest planet is unowned
                        target_planet = closest_planets[0]
                        if ship.can_dock(target_planet):
                            command_queue.append(ship.dock(target_planet))
                        else:
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_planet),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                    else: # closest planet is enemy
                        target_ship = closest_enemy_ships[0]
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)
                        if navigate_command:
                            command_queue.append(navigate_command)
                else:
                    if len(closest_planets[0].all_docked_ships()) < closest_planets[0].num_docking_spots:# if that planet is below dock threshold
                        target_planet = closest_planets[0] # dock with it
                        if ship.can_dock(target_planet):
                            command_queue.append(ship.dock(target_planet))
                        else:
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_planet),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                    elif closest_planets[1] is closest_enemy_planets[0]: # the 2nd closest planet is an enemy planet, attack w/o a dock check
                        target_ship = closest_enemy_ships[0] # attack w/o a dock check
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed = int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)
                        if navigate_command:
                            command_queue.append(navigate_command)
                    else: # default for this clause, means 2nd closest planet is mine
                        target_planet = closest_planets[1]
                        if len(target_planet.all_docked_ships()) < target_planet.num_docking_spots: # planet is below dock threshold
                            # dock at the planet
                            if ship.can_dock(target_planet):
                                command_queue.append(ship.dock(target_planet))
                            else:
                                navigate_command = ship.navigate(
                                    ship.closest_point_to(target_planet),
                                    game_map,
                                    speed = int(hlt.constants.MAX_SPEED),
                                    ignore_ships=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                        else: # planet was above dock threshold, go attack
                            target_ship = closest_enemy_ships[0]
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed = int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)
                            if navigate_command:
                                command_queue.append(navigate_command)
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
