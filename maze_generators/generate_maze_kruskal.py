from random import shuffle

SIZE = 51
START = (1, 1)
END = (SIZE-3, SIZE-3)


def generate_maze_kruskal(width=SIZE, height=SIZE, start=START, end=END):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)
    sets = [[i] for i in range(width * height)]  # Create disjoint sets for each cell

    def find_set(x):
        for i, s in enumerate(sets):
            if x in s:
                return i

    def union_set(x, y):
        set_x = find_set(x)
        set_y = find_set(y)
        sets[set_x] += sets[set_y]
        sets.pop(set_y)

    walls = []
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            if x > 0:
                walls.append((x - 1, y, x, y))  # Vertical wall
            if y > 0:
                walls.append((x, y - 1, x, y))  # Horizontal wall

    shuffle(walls)

    start_x, start_y = start
    end_x, end_y = end
    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3

    for wall in walls:
        x1, y1, x2, y2 = wall
        set1 = find_set(y1 * width // 2 + x1 // 2)
        set2 = find_set(y2 * width // 2 + x2 // 2)

        if set1 != set2:
            maze[y1][x1] = maze[y2][x2] = 1  # Mark the cells as empty (1)
            union_set(y1 * width // 2 + x1 // 2, y2 * width // 2 + x2 // 2)

    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    return maze