from random import randint
import random


# Class to define structure of a node
class Node:
    def __init__(self, value=None,
                 next_element=None):
        self.val = value
        self.next = next_element


# Class to implement a stack
class stack:

    # Constructor
    def __init__(self):
        self.head = None
        self.length = 0

    # Put an item on the top of the stack
    def insert(self, data):
        self.head = Node(data, self.head)
        self.length += 1

    # Return the top position of the stack
    def pop(self):
        if self.length == 0:
            return None
        else:
            returned = self.head.val
            self.head = self.head.next
            self.length -= 1
            return returned

    # Return False if the stack is empty
    # and true otherwise
    def not_empty(self):
        return bool(self.length)

    # Return the top position of the stack
    def top(self):
        return self.head.val


# Function to generate the random maze
def random_maze_generator(r, c, P0, Pf):
    ROWS, COLS = r, c

    # Array with only walls (where paths will
    # be created)
    maze = list(list(0 for _ in range(COLS))
                for _ in range(ROWS))

    # Auxiliary matrices to avoid cycles
    seen = list(list(False for _ in range(COLS))
                for _ in range(ROWS))
    previous = list(list((-1, -1)
                         for _ in range(COLS)) for _ in range(ROWS))

    S = stack()

    # Insert initial position
    S.insert(P0)

    # Keep walking on the graph using dfs
    # until we have no more paths to traverse
    # (create)
    while S.not_empty():

        # Remove the position of the Stack
        # and mark it as seen
        x, y = S.pop()
        seen[x][y] = True

        # Check if it will create a cycle
        # if the adjacent position is valid
        # (is in the maze) and the position
        # is not already marked as a path
        # (was traversed during the dfs) and
        # this position is not the one before it
        # in the dfs path it means that
        # the current position must not be marked.

        # This is to avoid cycles with adj positions
        if (x + 1 < ROWS) and maze[x + 1][y] == 1 \
                and previous[x][y] != (x + 1, y):
            continue
        if (0 < x) and maze[x - 1][y] == 1 \
                and previous[x][y] != (x - 1, y):
            continue
        if (y + 1 < COLS) and maze[x][y + 1] == 1 \
                and previous[x][y] != (x, y + 1):
            continue
        if (y > 0) and maze[x][y - 1] == 1 \
                and previous[x][y] != (x, y - 1):
            continue

        # Mark as walkable position
        maze[x][y] = 1

        # Array to shuffle neighbours before
        # insertion
        to_stack = []

        # Before inserting any position,
        # check if it is in the boundaries of
        # the maze
        # and if it were seen (to avoid cycles)

        # If adj position is valid and was not seen yet
        if (x + 1 < ROWS) and seen[x + 1][y] == False:
            # Mark the adj position as seen
            seen[x + 1][y] = True

            # Memorize the position to insert the
            # position in the stack
            to_stack.append((x + 1, y))

            # Memorize the current position as its
            # previous position on the path
            previous[x + 1][y] = (x, y)

        if (0 < x) and seen[x - 1][y] == False:
            # Mark the adj position as seen
            seen[x - 1][y] = True

            # Memorize the position to insert the
            # position in the stack
            to_stack.append((x - 1, y))

            # Memorize the current position as its
            # previous position on the path
            previous[x - 1][y] = (x, y)

        if (y + 1 < COLS) and seen[x][y + 1] == False:
            # Mark the adj position as seen
            seen[x][y + 1] = True

            # Memorize the position to insert the
            # position in the stack
            to_stack.append((x, y + 1))

            # Memorize the current position as its
            # previous position on the path
            previous[x][y + 1] = (x, y)

        if (y > 0) and seen[x][y - 1] == False:
            # Mark the adj position as seen
            seen[x][y - 1] = True

            # Memorize the position to insert the
            # position in the stack
            to_stack.append((x, y - 1))

            # Memorize the current position as its
            # previous position on the path
            previous[x][y - 1] = (x, y)

        # Indicates if Pf is a neighbour position
        pf_flag = False
        while len(to_stack):

            # Remove random position
            neighbour = to_stack.pop(randint(0, len(to_stack) - 1))

            # Is the final position,
            # remember that by marking the flag
            if neighbour == Pf:
                pf_flag = True

            # Put on the top of the stack
            else:
                S.insert(neighbour)

        # This way, Pf will be on the top
        if pf_flag:
            S.insert(Pf)

    # Mark the initial position
    x0, y0 = P0
    xf, yf = Pf
    maze[x0][y0] = 2
    maze[xf][yf] = 3

    # Return maze formed by the traversed path
    return maze


def generate_maze_prim(width, height, start, end):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)

    start_x, start_y = start
    end_x, end_y = end
    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    frontier = [(start_x, start_y)]

    while frontier:
        current_x, current_y = frontier.pop(random.randint(0, len(frontier)-1))
        neighbors = [(current_x-2, current_y), (current_x+2, current_y),
                     (current_x, current_y-2), (current_x, current_y+2)]

        for nx, ny in neighbors:
            if nx >= 0 and nx < width and ny >= 0 and ny < height and maze[nx][ny] == 0:
                maze[nx][ny] = 1  # Mark the neighboring cell as empty (1)
                maze[current_y + (ny - current_y)//2][current_x + (nx - current_x)//2] = 1  # Mark the wall as empty (1)
                frontier.append((nx, ny))

    # need to check if the maze has a solution. If it doesn't -> make more ways or regenerate

    return maze



# import random
# import sys
#
# def generate_maze_prim(width, height, start, end):
#     maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)
#
#     start_x, start_y = start
#     end_x, end_y = end
#     maze[start_y][start_x] = 2  # Mark the start cell as 2
#     maze[end_y][end_x] = 3  # Mark the end cell as 3
#     frontier = [(start_x, start_y)]
#
#     while frontier:
#         index = random.randint(0, len(frontier)-1)
#         current_x, current_y = frontier.pop(index)  # Pop the element at the randomly chosen index
#         neighbors = [(current_x-2, current_y), (current_x+2, current_y),
#                      (current_x, current_y-2), (current_x, current_y+2)]
#
#         for nx, ny in neighbors:
#             if nx >= 0 and nx < width and ny >= 0 and ny < height and maze[ny][nx] == 0:
#                 maze[ny][nx] = 1  # Mark the neighboring cell as empty (1)
#                 maze[current_y + (ny - current_y)//2][current_x + (nx - current_x)//2] = 1  # Mark the wall as empty (1)
#                 frontier.append((nx, ny))
#
#     # Check if the maze has a solution
#     sys.setrecursionlimit(width * height)  # Adjust recursion limit
#     if not find_path(maze, start, end):
#         # If the maze doesn't have a solution, regenerate the maze
#         return generate_maze_prim(width, height, start, end)
#
#     return maze
#
# def find_path(maze, start, end):
#     visited = set()
#
#     def dfs(x, y):
#         if (x, y) == end:
#             return True
#
#         visited.add((x, y))
#         for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
#             nx, ny = x + dx, y + dy
#             if (
#                 0 <= nx < len(maze[0])
#                 and 0 <= ny < len(maze)
#                 and maze[ny][nx] in [0, 3]
#                 and (nx, ny) not in visited
#             ):
#                 if dfs(nx, ny):
#                     return True
#
#         return False
#
#     start_x, start_y = start
#     return dfs(start_x, start_y)
#
# # Example usage:
# maze = generate_maze_prim(10, 10, (0, 0), (9, 9))
# print(maze)







def generate_maze_backtracking(width, height, start, end):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)

    def backtrack(x, y):
        maze[y][x] = 1  # Mark the current cell as empty (1)
        directions = [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]
        random.shuffle(directions)

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


def generate_maze_kruskal(width, height, start, end):
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

    random.shuffle(walls)

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


def generate_maze_backtracking2(width, height, start, end):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with all walls (0)

    def backtrack(x, y):
        maze[y][x] = 1  # Mark the current cell as empty (1)
        directions = [(x-2, y), (x+2, y), (x, y-2), (x, y+2)]
        random.shuffle(directions)

        for nx, ny in directions:
            if nx >= 0 and nx < width and ny >= 0 and ny < height and maze[ny][nx] == 0:
                maze[ny][nx] = 1  # Mark the next cell as empty (1)
                maze[y + (ny - y)//2][x + (nx - x)//2] = 1  # Mark the wall as empty (1)
                backtrack(nx, ny)

    start_x, start_y = start
    end_x, end_y = end
    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    backtrack(start_x, start_y)

    maze[start_y][start_x] = 2  # Mark the start cell as 2
    maze[end_y][end_x] = 3  # Mark the end cell as 3
    return maze



def generate_maze_kruskal2(width, height, start, end):
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

    random.shuffle(walls)

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


def generate_eller_maze(width, height, start, end):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with walls (0s)

    start_x, start_y = start
    end_x, end_y = end

    maze[start_y][start_x] = 2  # Mark start cell as 2
    maze[end_y][end_x] = 3  # Mark end cell as 3

    sets = [[i for i in range(width)]]

    for y in range(height - 1):
        row = []

        for x in range(width):
            row.append(x)
            if x < width - 1 and random.choice([True, False]):
                sets.append([len(sets)])
                row[-1] = len(sets) - 1

        for x in range(width):
            if x < width - 1 and row[x] != row[x + 1] and random.choice([True, False]):
                maze[y][x] = 1  # Mark the wall as empty (1)
                maze[y + 1][x] = 1  # Mark the cell below the wall as empty (1)
                row[x + 1] = row[x]

        for x in range(width):
            maze[y][x] = row[x]

    return maze


def generate_wilson_maze(width, height, start, end):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with walls (0s)

    start_x, start_y = start
    end_x, end_y = end

    maze[start_y][start_x] = 2  # Mark start cell as 2
    maze[end_y][end_x] = 3  # Mark end cell as 3

    unvisited = set((x, y) for x in range(width) for y in range(height))
    unvisited.remove((start_x, start_y))

    while unvisited:
        x, y = random.choice(list(unvisited))
        path = [(x, y)]
        visited = set()
        visited.add((x, y))

        while (x, y) in unvisited:
            nx, ny = random.choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) in visited:
                    path = path[:path.index((nx, ny)) + 1]
                else:
                    path.append((nx, ny))
                    visited.add((nx, ny))
            x, y = path[-1]

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            maze[y1][x1] = 1  # Mark the wall as empty (1)
            maze[y2][x2] = 1  # Mark the cell as empty (1)
            unvisited.remove((x1, y1))

    return maze


def check_maze(width, height, start, end):
    start_x, start_y = start
    end_x, end_y = end
    # Perform a search algorithm from the start point to connect it to the rest of the maze
    visited = [[False] * width for _ in range(height)]

    def dfs(x, y):
        visited[y][x] = True

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and maze[ny][nx] == 1:
                dfs(nx, ny)

    dfs(start_x, start_y)

    # Check if the end point is reachable from the start point
    if not visited[end_y][end_x]:
        # If the end point is not reachable, regenerate the maze
        return False
    return True


def print_maze(maze):
    for line in maze:
        print(line)


# Driver code
if __name__ == "__main__":
    N = 51
    M = 51
    P0 = (0, 0)
    P1 = (49, 49)
    # print("Random")
    # maze = random_maze_generator(N, M, P0, P1)
    # print_maze(maze)
    # print()
    print("Prim")
    maze = generate_maze_prim(N, M, P0, P1)
    print_maze(maze)
    # print()
    # print("backtracking")
    # maze = generate_maze_backtracking(N, M, P0, P1)
    # print_maze(maze)
    # print()
    # print("Kruskal")
    # maze = generate_maze_kruskal(N, M, P0, P1)
    # print_maze(maze)
    # print()
    # print("backtracking2")
    # maze = generate_maze_backtracking2(N, M, P0, P1)
    # print_maze(maze)
    # print()
    # print("Kruskal2")
    # maze = generate_maze_kruskal2(N, M, P0, P1)
    # print_maze(maze)
    # print()
    # print("Eller")
    # maze = random_maze_generator(N, M, P0, P1)
    # print_maze(maze)
    # print()
    # print("Wilson")
    # maze = random_maze_generator(N, M, P0, P1)
    # print_maze(maze)
    # print()