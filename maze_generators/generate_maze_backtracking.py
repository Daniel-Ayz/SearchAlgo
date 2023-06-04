from random import shuffle

SIZE = 51
START = (1, 1)
END = (SIZE-3, SIZE-3)


def generate_maze_backtracking(width=SIZE, height=SIZE, start=START, end=END):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)

    def backtrack(x, y):
        maze[y][x] = 1  # Mark the current cell as empty (1)
        directions = [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]
        shuffle(directions)

        for nx, ny in directions:
            if nx >= 0 and nx < width and ny >= 0 and ny < height and maze[ny][nx] == 0:
                maze[ny][nx] = 1  # Mark the next cell as empty (1)
                maze[y + (ny - y) // 2][x + (nx - x) // 2] = 1  # Mark the wall as empty (1)
                backtrack(nx, ny)

    start_x, start_y = start
    end_x, end_y = end
    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    backtrack(start_x, start_y)

    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    return maze