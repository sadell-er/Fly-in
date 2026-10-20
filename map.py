from hub_parser import Hub


class Map:
    def __init__(self, path: str) -> None:
        self.path = path
        self.nb_drones = 0
        self.lst_hub = []
        self.lst_conn = []

    def parse(self) -> None:
        indx = 0
        with open(self.path, "r") as f:
            for i, r in enumerate(f, start=1):
                if r[0] != '\n':
                    two = r.split("[")
                    w = two[0].split()
                    if w[0] == "#":
                        continue
                    elif w[0] == "nb_drones:":
                        nb_drones = w[1:]
                        self.nb_drones = nb_drones[0]
                        # print(self.nb_drones)

                    elif w[0] == "start_hub:":
                        start_hub = w[1:]
                        if len(two) != 2:
                            metatemp = None
                        else:
                            metatemp = two[1]
                        self.lst_hub.append(self.create_hub(start_hub,
                                                            metatemp, "start"))
                        print("stampa per controllo creazione start hub")
                        print(self.lst_hub[indx].metadata)
                        indx += 1

                    elif w[0] == "hub:":
                        hub = w[1:]
                        if len(two) != 2:
                            metatemp = None
                        else:
                            metatemp = two[1]
                        self.lst_hub.append(self.create_hub(hub,
                                                            metatemp, "hub"))
                        print("stampa per controllo creazione hub")
                        print(self.lst_hub[indx].metadata)
                        indx += 1

                    elif w[0] == "end_hub:":
                        end_hub = w[1:]
                        if len(two) != 2:
                            metatemp = None
                        else:
                            metatemp = two[1]
                        self.lst_hub.append(self.create_hub(end_hub,
                                                            metatemp, "end"))
                        print("stampa per controllo creazione end hub")
                        print(self.lst_hub[indx].metadata)
                        indx += 1

                    elif w[0] == "connection:":
                        connection = w[1:]
                        # print(connection)

    def create_hub(self, info: list, meta_data_str: str | None,
                   type: str) -> Hub:
        metadata_dict = {}
        for i, data in enumerate(info):
            try:
                temp_coord = int(data)
                if i == 1:
                    x = temp_coord
                elif i == 2:
                    y = temp_coord
                else:
                    print("Error: coords not in the right order")
            except ValueError:
                if i == 0:
                    name = data
                else:
                    print("Error: wrong name or metadata order")
                continue
        if meta_data_str:
            temp_lst = meta_data_str.strip().rstrip("]").split()
            for elem in temp_lst:
                temp_elem = elem.split("=")
                metadata_dict[temp_elem[0]] = temp_elem[1]
        hub = Hub(name, x, y, metadata_dict, type)
        return hub
