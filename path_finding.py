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
        target = Hub
        return target

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
