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
                        data = r.split()
                        if data[0] == "#":
                            continue
                        elif data[0] == "nb_drones:":
                            if flag != 0:
                                self.error_exit("wrong input order", i)
                            flag = 1
                            if len(data) != 2:
                                self.error_exit("wrong nb_drones input")
                            try:
                                self.nb_drones = int(data[1])
                                if self.nb_drones < 0:
                                    self.error_exit("nb_drones is negative", i)
                            except ValueError:
                                self.error_exit("nb_drones is not a number", i)
                            # print(self.nb_drones)

                        elif data[0] == "start_hub:":
                            metatmp = self.check_hub(data, i)
                            if flag != 1:
                                self.error_exit("wrong input order", i)
                            flag = 2
                            # print(data[1:4])
                            # print(metatmp)
                            hub = self.create_hub(data[1:4], metatmp,
                                                  "start", i)
                            self.lst_hub.append(hub)
                            # print("stampa per controllo creazione start hub")
                            # print(self.lst_hub[indx].metadata)
                            indx += 1

                        elif data[0] == "hub:":
                            metatmp = self.check_hub(data, i)
                            if flag != 2:
                                self.error_exit("wrong input order", i)
                            hub = self.create_hub(data[1:4], metatmp, "hub", i)
                            self.lst_hub.append(hub)
                            # print("stampa per controllo creazione hub")
                            # print(self.lst_hub[indx].metadata)
                            indx += 1

                        elif data[0] == "end_hub:":
                            metatmp = self.check_hub(data, i)
                            if flag != 2:
                                self.error_exit("wrong input order", i)
                            flag = 3
                            hub = self.create_hub(data[1:4], metatmp, "end", i)
                            self.lst_hub.append(hub)
                            # print("stampa per controllo creazione end hub")
                            # print(self.lst_hub[indx].metadata)
                            indx += 1

                        elif data[0] == "connection:":
                            if flag != 3:
                                self.error_exit("wrong input order", i)
                            metatmp = self.check_connection(data, i)
                            conn = self.create_connection(data[1], metatmp, i)
                            self.lst_conn.append(conn)
                            # print(conn.name1, conn.name2, conn.max)

                        else:
                            self.error_exit("wrong line text", i)
        except FileNotFoundError:
            self.error_exit("wrong path")
        if len(self.lst_hub) < 2 or self.lst_conn == 0:
            self.error_exit("not enough parameters")

        for h in self.lst_hub:
            print(h.name)
            print("=")
            for c in h.hub_conn:
                print(c)
            print()

    def check_hub(self, data: list, i: int) -> str:
        meta_str = ""
        if (len(data) < 3 or len(data) > 7):
            self.error_exit("wrong input", i)
        if len(data) > 4:
            if data[4][0] != "[" or data[-1][-1] != "]":
                self.error_exit("missing metadata brakets", i)
            for elem in data[4:]:
                meta_str += elem
            meta_str = meta_str[1:-1]
        return meta_str

    def check_connection(self, data: list, i: int) -> str:
        meta_str = ""
        if len(data[1].split("-")) != 2:
            self.error_exit("wrong number of links", i)
        if len(data) > 2:
            if len(data[2:]) > 1:
                self.error_exit("too many metadata", i)
            meta_str = data[2]
        return meta_str[1:-1]

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
                    for hubs in self.lst_hub:
                        if hubs.name == data:
                            self.error_exit("same hub name", line)
                    name = data
                else:
                    self.error_exit("wrong hub's data", line)
        for h in self.lst_hub:
            if h.x == x and h.y == y:
                self.error_exit("same coordinates from different hubs", line)
        if meta_data_str:
            temp_lst = meta_data_str.split()
            for elem in temp_lst:
                temp_elem = elem.split("=")
                metadata_dict[temp_elem[0]] = temp_elem[1]
        hub = Hub(name, x, y, metadata_dict, type)
        return hub

    def create_connection(self, conn_data: str, meta_data: str | None,
                          line: int) -> Connection:
        temp_conn = conn_data.split("-")
        if len(temp_conn) != 2:
            self.error_exit("not the right number of links", line)
        check = 0
        for hub in self.lst_hub:
            if hub.name == temp_conn[0]:
                check += 1
                tmp_hub1 = hub
            elif hub.name == temp_conn[1]:
                check += 1
                tmp_hub2 = hub
        if check != 2:
            self.error_exit("not the right name of links", line)
        tmp_hub1.hub_conn.append(temp_conn[1])
        tmp_hub2.hub_conn.append(temp_conn[0])
        if meta_data:
            temp_lst = meta_data.split()
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
        for conn in self.lst_conn:
            if conn.name1 == temp_conn[0] or conn.name1 == temp_conn[1]:
                if conn.name2 == temp_conn[0] or conn.name2 == temp_conn[1]:
                    self.error_exit("same connection repeated", line)
        conn = Connection(temp_conn[0], temp_conn[1], meta_data)
        return conn

    def error_exit(self, error: str, line: int | None) -> None:
        if line:
            print(f"[ERROR](line {line}): {error}")
        else:
            print(f"[ERROR]: {error}")
        exit()
