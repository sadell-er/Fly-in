from map import Map
from hub import Hub, Connection, Drone


class Path:
    def __init__(self, path: list[Hub | Connection], max_drones: int,
                 cost: int) -> None:
        self.lst = path
        self.max_drones = max_drones
        self.cost = cost
        self.drones = 0
        self.time = 0


class Algorithm:
    def __init__(self, map: Map) -> None:
        self.map = map
        self.paths_lst = []

    def algorithm(self) -> None:
        if not self.path_finder():
            print("[ERROR]: end_hub is not connected to start_hub")
            exit()
        while True:
            path = self.path_finder()
            if not path:
                break
        # assegno ad ogni drone il proprio percorso
        self.assign_drones()
        turns = 0
        while len(self.map.lst_hub[-1].curr_drones) != self.map.nb_drones:
            print(f"\nTurn: {turns + 1}")
            turns += self.move_drones()
        print(f"\n\nTOT turns = {turns}")

    # PATH FINDER #

    def path_finder(self) -> list[Hub | Connection | None]:
        lst_hub = self.map.lst_hub
        end = lst_hub[-1]
        start = lst_hub[0]
        current = start
        visited = []
        seen = set(n for n in start.neighbours if n.zone != "blocked"
                   and n.capacity > 0)
        path = []

        # resetto i dati degli hub per il calcolo del percorso
        for hub in lst_hub:
            hub.cost = 0
            hub.parent = None
            hub.parent_conn = None

        while current != end:
            # si assegna il costo ad i vicini connessi e con capienza
            for conn in current.hub_conn:
                if conn.hub1 == current:
                    neighbor = conn.hub2
                else:
                    neighbor = conn.hub1
                if neighbor != start and neighbor.zone != "blocked" \
                   and neighbor.capacity > 0 and conn.capacity > 0:
                    sum = current.cost + neighbor.turn
                    if sum < neighbor.cost or neighbor.cost == 0:
                        neighbor.cost = sum
                        neighbor.parent = current
                        neighbor.parent_conn = conn

            # salvo l'hub con il costo minore tra quelli visti finora
            less = None
            for hub in seen:
                if less is None or hub.cost < less.cost:
                    less = hub

            # Se less è None o 0, non ci sono più strade
            if less is None or less.cost == 0:
                return []

            # aggiungo l'hub con il costo minore alla lista dei visitati,
            # lo rimuovo dai visti e aggiorno seen
            visited.append(less)
            seen.remove(less)
            current = less
            seen.update(n for n in less.neighbours if n not in visited
                        and n != start and n.zone != "blocked"
                        and n.capacity > 0)

        # ricostruisco il percorso
        while current != start:
            path.append(current)
            if current.parent.zone == "restricted":
                path.append(current.parent_conn)
            current = current.parent
        # path.append(start)
        path.reverse()
        # trovo la max capacity del percoso e modifico le capacità di tutti
        # gli elementi del path
        flow_capacity = self.find_flow_capacity(path)
        for zone in path:
            if zone != self.map.lst_hub[0] and zone != self.map.lst_hub[-1]:
                zone.capacity -= flow_capacity

        final_path = Path(path, flow_capacity, end.cost)
        self.paths_lst.append(final_path)
        return path

    def find_flow_capacity(self, path: list[Hub | Connection]) -> int:
        max_drones = float('inf')
        for zone in path:
            if zone != self.map.lst_hub[0] and zone != self.map.lst_hub[-1]:
                if zone.capacity < max_drones:
                    max_drones = zone.capacity
        return max_drones

    def assign_drones(self) -> None:
        for drone in self.map.lst_drones:
            min_time = 99999
            for path in self.paths_lst:
                path.time = path.cost + (path.drones / path.max_drones)
                if path.time < min_time:
                    min_time = path.time
                    best_path = path
            best_path.drones += 1
            drone.path = best_path.lst.copy()

    def move_drones(self) -> int:
        for drone in self.map.lst_drones:
            if isinstance(drone.position, Hub):
                if drone.position.type == "end":
                    continue
            target = drone.path[0]
            if isinstance(target, Hub) and target.type == "end":
                self.one_move(drone, target)
            elif len(target.curr_drones) < target.max_drones:
                self.one_move(drone, target)
                drone.path.pop(0)
        return 1

    def one_move(self, drone: Drone, target: Hub | Connection) -> None:
        try:
            drone.position.curr_drones.remove(drone)
        except ValueError as e:
            print(e)
        target.curr_drones.append(drone)
        drone.position = target
        # print ufficiale
        print(f"{drone.id}-{drone.position.name}")

# PRINT #

    # stampo i percorsi assegnati ai droni
    def print_drones_paths(self) -> None:
        for drone in self.map.lst_drones:
            if drone.path:
                print(f"Drone {drone.id} assigned to path: ")
                self.print_single_path(drone.path)
            else:
                print(f"Drone {drone.id} has no assigned path")

    # stampo un singolo percorso con la sua capacità massima
    def print_single_path(self, path_obj: Path) -> None:
        print()
        print()
        print(f"Path:  (max_drones = {path_obj.max_drones})")
        for index, p in enumerate(path_obj.lst):
            if index == len(path_obj.lst) - 1:
                end = ""
            else:
                end = " -> "
            print(f"{p.name}", end=end)

    def print_paths(self) -> None:
        for path_obj in self.paths_lst:
            self.print_single_path(path_obj)
            print()
            print(f"Number of drones assigned: {path_obj.drones}")
