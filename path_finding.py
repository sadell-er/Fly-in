from map import Map
from hub import Drone, Hub, Connection


class Algorithm:
    def __init__(self, map: Map) -> None:
        self.map = map

    def alg(self) -> None:
        if self.a_star(self.map.lst_drones[0]) is None:
            print("[ERROR]: end_hub is not connected to start_hub")
            exit()
        turns = 0
        while len(self.map.lst_hub[-1].curr_drones) != self.map.nb_drones:
            self.one_turn()
            turns += 1

    def one_turn(self) -> None:
        for drone in self.map.lst_drones:
            target = self.a_star(drone)
            if target is None:
                continue
            self.move_drone(drone, target)

    def a_star(self, drone: Drone) -> Hub | Connection | None:
        if isinstance(drone.position, Connection):
            return drone.position.dest
        i = 0
        lst_hub = self.map.lst_hub
        lst_conn = self.map.lst_conn
        end = lst_hub[-1]
        start = lst_hub[0]
        curr_pos = drone.position
        visited = ()
#        for conn in lst_conn:
#            if conn.hub2.name == end.name or conn.hub1.name == end.name:
#                for hub in lst_hub:
#                    if (hub.name == conn.hub1.name and hub.name != end.name) \
#                       or (hub.name == conn.hub2.name
#                           and hub.name != end.name):
#                        curr_hub = hub
#                while curr_hub != lst_hub[0]:
#                    if lst_conn[i].hub2.name == curr_hub.name:
#                        for hub in lst_hub:
#                            if hub.name == lst_conn[i].hub1.name:
#                                curr_hub = hub
#                    elif lst_conn[i].hub1.name == curr_hub.name:
#                        for hub in lst_hub:
#                            if hub.name == lst_conn[i].hub2.name:
#                                curr_hub = hub
#                    else:
#                        continue
#                    i += 1
#                i = 0
        return target

    def find_max_capacity(self) -> int:
        max_hub = 0
        for hub in self.map.lst_hub[1:-1]:
            if max_hub < hub.max_drones:
                max_hub = hub.max_drones
        max_conn = 0
        for conn in self.map.lst_conn:
            if max_conn < conn.max_link_capacity:
                max_conn = conn.max_link_capacity
        if max_conn <= max_hub:
            return max_hub
        else:
            return max_conn

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
