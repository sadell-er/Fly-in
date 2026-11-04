# from hub_parser import Hub
from map import Map
from path_finding import Algorithm


def main() -> None:
    easy1 = "maps/easy/01_linear_path.txt"
    easy2 = "maps/easy/02_simple_fork.txt"
    easy3 = "maps/easy/03_basic_capacity.txt"
    medium1 = "maps/medium/01_dead_end_trap.txt"
    medium2 = "maps/medium/02_circular_loop.txt"
    medium3 = "maps/medium/03_priority_puzzle.txt"
    hard1 = "maps/hard/01_maze_nightmare.txt"
    hard3 = "maps/hard/03_ultimate_challenge.txt"
    map = Map(easy2)
    map.parse()
    alg = Algorithm(map)
    alg.alg()
    # alg.move_drone(map.lst_drones[0], map.lst_hub[0])
    # map.view_drones()

    return


if __name__ == "__main__":
    main()
