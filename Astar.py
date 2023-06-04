import time

import pygame
import math
from queue import PriorityQueue

WIDTH = 500

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def manhattan(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2) * 1.001


def euclidean(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) * 1.001


def reconstruct_path(came_from, current, draw):
	count = 0
	while current in came_from:
		count += 1
		current = came_from[current]
		current.make_path()
		draw()
	print(count)


def algorithm(draw, grid, h, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	# open_set.put((0, count), start)
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.event.post(pygame.event.Event(pygame.QUIT))
				return False

		current = open_set.get()[2]
		# current = open_set.get()[1]
		open_set_hash.remove(current)

		if current == end:
			draw()
			reconstruct_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			if neighbor.is_closed():
				continue
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					# open_set.put((f_score[neighbor], count), neighbor)
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def validate_click(row, col, max_len):
	return 0 <= row < max_len and 0 <= col < max_len


def main(win, width, h=manhattan):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				if not validate_click(row, col, ROWS):
					continue
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				if not validate_click(row, col, ROWS):
					continue
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					for row in grid:
						for spot in row:
							if not spot.is_barrier():
								if not spot.is_start() and not spot.is_end():
									spot.reset()
								spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, manhattan, start, end)
					time.sleep(5)
					for row in grid:
						for spot in row:
							if not spot.is_barrier():
								if not spot.is_start() and not spot.is_end():
									spot.reset()
								spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, euclidean, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()


def run_algo_from_grid(win, grid, h, rows, width, start, end):
	run = True
	while run:
		draw(win, grid, rows, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				for row in grid:
					for spot in row:
						if not spot.is_barrier():
							if not spot.is_start() and not spot.is_end():
								spot.reset()
							spot.update_neighbors(grid)

				for row in grid:
					for spot in row:
						if not spot.is_barrier():
							if not spot.is_start() and not spot.is_end():
								spot.reset()
							spot.update_neighbors(grid)
				print("manhattan")
				start_t = time.time()
				algorithm(lambda: draw(win, grid, rows, width), grid, manhattan, start, end)
				end_t = time.time()
				print("run time: ", end_t - start_t)
				time.sleep(5)
				for row in grid:
					for spot in row:
						if not spot.is_barrier():
							if not spot.is_start() and not spot.is_end():
								spot.reset()
							spot.update_neighbors(grid)
				print("euclidian")
				start_t = time.time()
				algorithm(lambda: draw(win, grid, rows, width), grid, euclidean, start, end)
				end_t = time.time()
				print("run time: ", end_t-start_t)

				# algorithm(lambda: draw(win, grid, rows, width), grid, h, start, end)
	pygame.quit()


if "__main__" == __name__:
	main(WIN, WIDTH)