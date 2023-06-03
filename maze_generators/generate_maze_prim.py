from random import randint
from maze_tools import print_maze
SIZE = 51
START = (1, 1)
END = (SIZE-3, SIZE-3)


def generate_maze_prim(width=SIZE, height=SIZE, start=START, end=END):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)

    start_x, start_y = start
    end_x, end_y = end
    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    frontier = [(start_x, start_y)]

    while frontier:
        current_x, current_y = frontier.pop(randint(0, len(frontier)-1))
        neighbors = [(current_x-2, current_y), (current_x+2, current_y),
                     (current_x, current_y-2), (current_x, current_y+2)]

        for nx, ny in neighbors:
            if nx >= 0 and nx < width and ny >= 0 and ny < height and maze[nx][ny] == 0:
                maze[nx][ny] = 1  # Mark the neighboring cell as empty (1)
                maze[current_y + (ny - current_y)//2][current_x + (nx - current_x)//2] = 1  # Mark the wall as empty (1)
                frontier.append((nx, ny))

    return maze


if __name__ == "__main__":
    print("Prim Maze")
    maze = generate_maze_prim()
    print_maze(maze)