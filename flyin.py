# from hub_parser import Hub
from map import Map


def main() -> None:
    easy1 = "maps/easy/01_linear_path.txt"
    easy3 = "maps/easy/03_basic_capacity.txt"
    hard3 = "maps/hard/03_ultimate_challenge.txt"
    mappa = Map(hard3)
    mappa.parse()
    return


if __name__ == "__main__":
    main()
