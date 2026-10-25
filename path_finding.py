from map import Map
from hub import Drone, Hub, Connection


class Algorithm:
    def __init__(self, map: Map) -> None:
        self.map = map

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
