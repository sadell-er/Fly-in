# from .hub_parser import Hub


def parse() -> None:
    with open("maps/easy/01_linear_path.txt", "r") as f:
        for r in f:
            if r[0] != '\n':
                w = r.split()
                if w[0] == "#":
                    continue
                elif w[0] == "nb_drones:":
                    nb_drones = w[1:]
                    print(nb_drones)
                elif w[0] == "start_hub:":
                    start_hub = w[1:]
                    print(start_hub)
                elif w[0] == "hub:":
                    hub = w[1:]
                    print(hub)
                elif w[0] == "end_hub:":
                    end_hub = w[1:]
                    print(end_hub)
                elif w[0] == "connection:":
                    connection = w[1:]
                    print(connection)


def main() -> None:
    parse()
    return


if __name__ == "__main__":
    main()
