class Hub:
    def __init__(self, name: str, x: int, y: int,
                 metadata: dict[str: str] | None, type: str) -> None:
        self.type = type
        self.name = name
        self.turn = 0
        self.x = x
        self.y = y
        self.color = None
        self.metadata = metadata
        self.zone = "normal"
        if type == "hub":
            self.turn = 1
            self.max_drones = 1
        if type != "start":
            self.capacity = 1
        self.hub_conn = []
        self.curr_drones = []
        self.neighbours = []
        self.cost = 0
        self.parent = None
        self.parent_conn = None

    def metadata_parser(self, line: int) -> None:
        if self.type != "hub":
            if self.metadata:
                if len(self.metadata) > 2:
                    print(f"[ERROR](line {line}): too many metadata")
                    exit()
                for k, v in self.metadata.items():
                    if k == "color":
                        self.color = v
                    elif k == "max_drones":
                        continue
                    else:
                        print(f"[ERROR](line {line}): wrong metadata name "
                              "(should be 'color')")
                        exit()
            return
        for k, v in self.metadata.items():
            if k == "zone":
                if v == "normal":
                    self.zone = "normal"
                    self.turn = 1
                elif v == "blocked":
                    self.zone = "blocked"
                    self.turn = 99999
                elif v == "restricted":
                    self.zone = "restricted"
                    self.turn = 2
                elif v == "priority":
                    self.zone = "priority"
                    self.turn = 0.9
                else:
                    print(f"[ERROR](line {line}): wrong zone name")
                    exit()
            elif k == "color":
                self.color = v
            elif k == "max_drones":
                try:
                    n = int(v)
                    if n <= 0:
                        raise ValueError
                except ValueError:
                    print(f"[ERROR](line {line}): wrong value for max_drones")
                    exit()
                self.max_drones = n
                self.capacity = n
            else:
                print(f"[ERROR](line {line}): wrong name of metadata")
                exit()


class Connection:
    def __init__(self, hub1: Hub, hub2: Hub,
                 max_link_capacity: int | None) -> None:
        self.hub1 = hub1
        self.hub2 = hub2
        self.name = f"{hub1.name}-{hub2.name}"
        self.capacity = 1
        self.max_drones = 1
        self.curr_drones = []
        if max_link_capacity:
            self.max_drones = max_link_capacity
            self.capacity = max_link_capacity
        hub1.neighbours.append(hub2)
        hub2.neighbours.append(hub1)


class Drone:
    def __init__(self, id: str, position: Hub | Connection) -> None:
        self.id = id
        self.position = position
        self.path = []
        # self.target = target
