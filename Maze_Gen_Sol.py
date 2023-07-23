from search_algorithms.Astar import algorithm as astar
from grid.grid_visualizer import run_algorithm_from_grid, make_grid
from maze_generators.generate_maze_prim import generate_maze_prim
from maze_generators.generate_maze_dfs import generate_maze_dfs
from maze_generators.generate_maze_backtracking import generate_maze_backtracking
from maze_generators.generate_maze_kruskal import generate_maze_kruskal


SIZE = 51
WIDTH = 10 * SIZE
START = (1, 1)
END = (SIZE-3, SIZE-3)


def print_gen_maze(maze):
    for line in maze:
        print(line)


def convert_maze_to_grid(maze):
    grid = make_grid(SIZE, WIDTH)
    for x, line in enumerate(grid):
        for y, slot in enumerate(line):
            sign = maze[x][y]
            if sign == 2:
                slot.make_start()
            elif sign == 3:
                slot.make_end()
            elif sign == 0:
                slot.make_barrier()
    return grid


def main():
    maze_dfs = generate_maze_dfs(SIZE, SIZE, START, END)
    maze_prim = generate_maze_prim(SIZE, SIZE, START, END)
    maze_backtracking = generate_maze_backtracking(SIZE, SIZE, START, END)
    maze_kruskal = generate_maze_kruskal(SIZE, SIZE, START, END)

    grid_dfs = convert_maze_to_grid(maze_dfs)
    grid_prim = convert_maze_to_grid(maze_prim)
    grid_backtracking = convert_maze_to_grid(maze_backtracking)
    grid_kruskal = convert_maze_to_grid(maze_kruskal)


    run_algorithm_from_grid(astar, grid_dfs, grid_dfs[START[0]][START[1]], grid_dfs[END[0]][END[1]])
    run_algorithm_from_grid(astar, grid_prim, grid_prim[START[0]][START[1]], grid_prim[END[0]][END[1]])
    run_algorithm_from_grid(astar, grid_backtracking, grid_backtracking[START[0]][START[1]], grid_backtracking[END[0]][END[1]])
    run_algorithm_from_grid(astar, grid_kruskal, grid_kruskal[START[0]][START[1]], grid_kruskal[END[0]][END[1]])



main()
