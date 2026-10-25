class Hub:
    def __init__(self, name: str, x: int, y: int,
                 metadata: dict[str: str] | None, type: str) -> None:
        self.type = type
        self.name = name
        self.x = x
        self.y = y
        self.color = None
        self.metadata = metadata
        if type == "hub":
            self.zone = "normal"
            self.turn = 1
            self.max_drones = 1
        self.hub_conn = []
        self.curr_drones = []

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
                    self.turn = 1
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
            else:
                print(f"[ERROR](line {line}): wrong name of metadata")
                exit()


class Connection:
    def __init__(self, name1: Hub, name2: Hub,
                 max_link_capacity: int | None) -> None:
        self.name1 = name1
        self.name2 = name2
        self.max = 1
        self.curr_drones = []
        if max_link_capacity:
            self.max = max_link_capacity


class Drone:
    def __init__(self, id: str, position: Hub | Connection) -> None:
        self.id = id
        self.position = position
        # self.target = target
