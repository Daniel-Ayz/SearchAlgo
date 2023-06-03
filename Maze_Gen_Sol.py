import pygame

from Astar import make_grid, Spot, run_algo_from_grid, manhattan, euclidean
from maze_generator import random_maze_generator

SIZE = 50
WIDTH = 10 * SIZE
START = (0, 0)
END = (SIZE-1, SIZE-1)


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
    maze = random_maze_generator(SIZE, SIZE, START, END)
    grid1 = convert_maze_to_grid(maze)
    grid2 = convert_maze_to_grid(maze)
    win = pygame.display.set_mode((WIDTH, WIDTH))
    run_algo_from_grid(win, grid1, manhattan, SIZE, WIDTH, grid1[START[0]][START[1]], grid1[END[0]][END[1]])

    win = pygame.display.set_mode((WIDTH, WIDTH))
    run_algo_from_grid(win, grid2, euclidean, SIZE, WIDTH, grid2[START[0]][START[1]], grid2[END[0]][END[1]])


main()
