from map import Map
from hub import Drone, Hub, Connection


class Algorithm:
    def __init__(self, map: Map) -> None:
        self.map = map

    def alg(self) -> None:
        if not self.path_finder(self.map.lst_drones[0]):
            print("[ERROR]: end_hub is not connected to start_hub")
            exit()
        turns = 0
        active_lst = []
        for drone in self.map.lst_drones:
            path = self.path_finder(drone)
            if not path:
                print("[ERROR]: start is not connected to end")
                exit()
            drone.path = path.reverse()
            active_lst.append(drone)
        while len(self.map.lst_hub[-1].curr_drones) != self.map.nb_drones:
            for drone in active_lst:
                if drone.path[0].curr_drones()
            turns += 1

    def path_finder(self, drone: Drone) -> list[Hub | Connection | None]:
        if isinstance(drone.position, Connection):
            return drone.position.dest
        lst_hub = self.map.lst_hub
        end = lst_hub[-1]
        curr_pos = drone.position
        visited = [curr_pos]
        seen = set(curr_pos.neighbours)
        path = []
        while seen:
            if end in seen:
                # da ritornare il path
                print(end.name)
                curr_pos = end
                while curr_pos != lst_hub[0]:
                    path.append(curr_pos)
                    for i, hub in enumerate(curr_pos.neighbours):
                        if i == 0:
                            back = hub
                        if hub.cost < back.cost:
                            back = hub
                    # check del max capacity, hub.ghost_drones, se len(ghost) 
                    # = max capacity -> cost +1 e ghost.clear(). Mettere i droni
                    # dentro connection se la dest è restricted e fare i 
                    # controlli quando li muovo
                    curr_pos.cost += 1
                    if back == lst_hub[0]:
                        return path
                    curr_pos = back

            for n in curr_pos.neighbours:
                sum = curr_pos.cost + n.turn
                if n.cost == 0 or sum < n.cost:
                    n.cost = sum
            for i, hub in enumerate(seen):
                if i == 0:
                    less = hub
                if hub.cost < less.cost:
                    less = hub
            visited.append(less)
            seen.remove(less)
            curr_pos = less

            seen.update(n for n in curr_pos.neighbours if n not in visited)
        return []

    def find_max_capacity(self, path: list[Hub | Connection]) -> int:
        max_zone = 0
        for zone in path:
            if isinstance(zone, Hub):
                if max_zone > zone.max_drones:
                    max_zone = zone.max_drones
            elif isinstance(zone, Connection):
                if max_zone > zone.max:
                    max_zone = zone.max
        return max_zone

    def move_drone(self, drone: Drone, target: Hub | Connection) -> None:
        try:
            drone.position.curr_drones.remove(drone)
        except ValueError as e:
            print(e)
        target.curr_drones.append(drone)
        drone.position = target
        print("posizione finale")
        self.print_positions()

    def print_positions(self) -> None:
        for i in self.map.lst_hub:
            print(f"[hub name]    = {i.name}")
            print("[curr drones] = ", end="{")
            print(*(d.id for d in i.curr_drones), sep=" - ", end="}\n\n")
