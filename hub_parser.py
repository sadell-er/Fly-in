class Hub:
    def __init__(self, name: str, x: int, y: int,
                 metadata: dict[str: str] | None, type: str) -> None:
        self.type = type
        self.name = name
        self.x = x
        self.y = y
        self.metadata = metadata
        self.color = None
        if type == "hub":
            self.zone = "normal"
            self.turn = 1
            self.max_drones = 1
            self.metadata_parser()
        elif metadata["color"]:
            self.color = metadata["color"]

        self.connections = list[None | Connection]

    def metadata_parser(self) -> None:
        for k, v in self.metadata.items():
            if k == "zone":
                if v == "normal":
                    self.zone = "normal"
                    self.turn = 1
                if v == "blocked":
                    self.zone = "blocked"
                    self.turn = 99999
                if v == "restricted":
                    self.zone = "restricted"
                    self.turn = 2
                if v == "priority":
                    self.zone = "priority"
                    self.turn = 1
            if k == "color":
                self.color = v
            if k == "max_drones":
                self.max_drones = v


class Connection:
    def _init__(self, name1: Hub, name2: Hub, max_link_capacity: int) -> None:
        self.name1 = name1
        self.name2 = name2
        self.max = max_link_capacity
