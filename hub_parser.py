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
        self.hub_conn = []

    def metadata_parser(self, line: int) -> None:
        if self.type != "hub":
            if self.metadata:
                if len(self.metadata) != 1:
                    print(f"[ERROR](line {line}): too many metadata")
                    exit()
                key = list(self.metadata.keys())
                if key[0] != "color":
                    print(f"[ERROR](line {line}): wrong metadata name "
                          "(should be 'color')")
                    exit()
                self.color = self.metadata["color"]
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
                    print(f"[ERROR](line {line}): wrong metadata name")
            elif k == "color":
                self.color = v
            elif k == "max_drones":
                self.mrones = v
            else:
                print(f"[ERROR](line {line}): wrong name of metadata")
                exit()


class Connection:
    def __init__(self, name1: Hub, name2: Hub,
                 max_link_capacity: int | None) -> None:
        self.name1 = name1
        self.name2 = name2
        self.max = 1
        if max_link_capacity:
            self.max = max_link_capacity
