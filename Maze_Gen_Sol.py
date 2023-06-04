import pygame

from Astar import make_grid, run_algo_from_grid, euclidean
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


def run_algo(grid):
    pass


def main():
    maze_dfs = generate_maze_dfs(SIZE, SIZE, START, END)
    maze_prim = generate_maze_prim(SIZE, SIZE, START, END)
    maze_backtracking = generate_maze_backtracking(SIZE, SIZE, START, END)
    maze_kruskal = generate_maze_kruskal(SIZE, SIZE, START, END)
    # maze_eller = generate_eller_maze(SIZE, SIZE, START, END)
    # print_gen_maze(maze_eller)
    # maze_wilson = maze_generator.generate_wilson_maze(SIZE, SIZE, START, END)


    grid_dfs = convert_maze_to_grid(maze_dfs)
    grid_prim = convert_maze_to_grid(maze_prim)
    grid_backtracking = convert_maze_to_grid(maze_backtracking)
    grid_kruskal = convert_maze_to_grid(maze_kruskal)
    # grid_eller = convert_maze_to_grid(maze_eller)
    # grid_wilson = convert_maze_to_grid(maze_wilson)


    win = pygame.display.set_mode((WIDTH, WIDTH))
    run_algo_from_grid(win, grid_dfs, euclidean, SIZE, WIDTH, grid_dfs[START[0]][START[1]], grid_dfs[END[0]][END[1]])
    #
    win = pygame.display.set_mode((WIDTH, WIDTH))
    run_algo_from_grid(win, grid_prim, euclidean, SIZE, WIDTH, grid_prim[START[0]][START[1]], grid_prim[END[0]][END[1]])
    #
    win = pygame.display.set_mode((WIDTH, WIDTH))
    run_algo_from_grid(win, grid_backtracking, euclidean, SIZE, WIDTH, grid_backtracking[START[0]][START[1]], grid_backtracking[END[0]][END[1]])
    #
    # win = pygame.display.set_mode((WIDTH, WIDTH))
    # run_algo_from_grid(win, grid_kruskal, euclidean, SIZE, WIDTH, grid_kruskal[START[0]][START[1]], grid_kruskal[END[0]][END[1]])

    # win = pygame.display.set_mode((WIDTH, WIDTH))
    # run_algo_from_grid(win, grid_eller, euclidean, SIZE, WIDTH, grid_eller[START[0]][START[1]], grid_eller[END[0]][END[1]])

    # win = pygame.display.set_mode((WIDTH, WIDTH))
    # run_algo_from_grid(win, grid_wilson, euclidean, SIZE, WIDTH, grid_wilson[START[0]][START[1]], grid_wilson[END[0]][END[1]])


main()
