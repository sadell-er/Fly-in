from hub_parser import Hub, Connection


class Map:
    def __init__(self, path: str) -> None:
        if path is None:
            self.error_exit("path not given")
        self.path = path
        self.nb_drones = 0
        self.lst_hub = []
        self.lst_conn = []

    def parse(self) -> None:
        indx = 0
        flag = 0
        try:
            with open(self.path, "r") as f:
                for i, r in enumerate(f, start=1):
                    if r[0] != '\n':
                        two = r.split("[")
                        if len(two) != 2:
                            metatemp = None
                        else:
                            metatemp = two[1]
                        w = two[0].split()
                        if w[0] == "#":
                            continue
                        elif w[0] == "nb_drones:":
                            if flag != 0:
                                self.error_exit("wrong input order", i)
                            flag = 1
                            nb_drones = w[1:]
                            self.nb_drones = nb_drones[0]
                            # print(self.nb_drones)

                        elif w[0] == "start_hub:":
                            if flag != 1:
                                self.error_exit("wrong input order", i)
                            flag = 2
                            hub = self.create_hub(w[1:], metatemp, "start", i)
                            self.lst_hub.append(hub)
                            # print("stampa per controllo creazione start hub")
                            # print(self.lst_hub[indx].metadata)
                            indx += 1

                        elif w[0] == "hub:":
                            if flag != 2:
                                self.error_exit("wrong input order", i)
                            hub = self.create_hub(w[1:], metatemp, "hub", i)
                            self.lst_hub.append(hub)
                            # print("stampa per controllo creazione hub")
                            # print(self.lst_hub[indx].metadata)
                            indx += 1

                        elif w[0] == "end_hub:":
                            if flag != 2:
                                self.error_exit("wrong input order", i)
                            flag = 3
                            hub = self.create_hub(w[1:], metatemp, "end", i)
                            self.lst_hub.append(hub)
                            # print("stampa per controllo creazione end hub")
                            # print(self.lst_hub[indx].metadata)
                            indx += 1

                        elif w[0] == "connection:":
                            if flag != 3:
                                self.error_exit("wrong input order", i)
                            conn = self.create_connection(w[1:], metatemp, i)
                            self.lst_conn.append(conn)
                            # print(conn.name1, conn.name2, conn.max)

                        else:
                            self.error_exit("wrong line text", i)
        except FileNotFoundError:
            self.error_exit("wrong path")
        if len(self.lst_hub) < 2 or self.lst_conn == 0:
            self.error_exit("not enough parameters")

    def create_hub(self, info: list, meta_data_str: str | None,
                   type: str, line: int) -> Hub:
        metadata_dict = {}
        for i, data in enumerate(info):
            try:
                temp_coord = int(data)
                if i == 1:
                    x = temp_coord
                elif i == 2:
                    y = temp_coord
                else:
                    self.error_exit("coords not in the right order", line)
            except ValueError:
                if i == 0:
                    name = data
                else:
                    self.error_exit("wrong name or metadata order", line)
        if meta_data_str:
            temp_lst = meta_data_str.strip().rstrip("]").split()
            for elem in temp_lst:
                temp_elem = elem.split("=")
                metadata_dict[temp_elem[0]] = temp_elem[1]
        hub = Hub(name, x, y, metadata_dict, type)
        return hub

    def create_connection(self, conn_data: list, meta_data: str | None,
                          line: int) -> Connection:
        if len(conn_data) != 1:
            self.error_exit("too many links", line)
        else:
            temp_conn = conn_data[0].split("-")
            if len(temp_conn) != 2:
                self.error_exit("not the right number of links", line)
            check = 0
            for hub in self.lst_hub:
                if hub.name == temp_conn[0]:
                    check += 1
                elif hub.name == temp_conn[1]:
                    check += 1
            if check != 2:
                self.error_exit("not the right name of links", line)
        if meta_data:
            temp_lst = meta_data.strip().rstrip("]").split()
            if len(temp_lst) != 1:
                self.error_exit("too much metadata", line)
            else:
                temp_elem = temp_lst[0].split("=")
                if temp_elem[0] != "max_link_capacity":
                    self.error_exit("not the right name (should be "
                                    "'max_link_capacity')", line)
                try:
                    meta_data = int(temp_elem[1])
                except ValueError:
                    self.error_exit("max link capacity is not a number", line)
        conn = Connection(temp_conn[0], temp_conn[1], meta_data)
        return conn

    def error_exit(self, error: str, line: int | None) -> None:
        if line:
            print(f"[ERROR](line {line}): {error}")
        else:
            print(f"[ERROR]: {error}")
        exit()
