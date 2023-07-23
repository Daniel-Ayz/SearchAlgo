import time
import pygame

ROWS = 51
WIDTH = ROWS * 10
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("grid visualizer")


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


def make_grid(rows=ROWS, width=WIDTH):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid


def draw_grid_pygame(win=WIN, rows=ROWS, width=WIDTH):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(grid, win=WIN, rows=ROWS, width=WIDTH):
	win.fill(WHITE)
	for row in grid:
		for spot in row:
			spot.draw(win)
	draw_grid_pygame(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows=ROWS, width=WIDTH):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def validate_click(row, col, max_len=ROWS):
	return 0 <= row < max_len and 0 <= col < max_len


def is_terminated():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.event.post(pygame.event.Event(pygame.QUIT))
			return True


def run_algorithm(algorithm):
	grid = make_grid()

	start = None
	end = None

	run = True
	while run:
		draw(grid)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos)
				if not validate_click(row, col):
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
				row, col = get_clicked_pos(pos)
				if not validate_click(row, col):
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

					algorithm(lambda: draw(grid), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid()

	# pygame.quit()


def run_algorithm_from_grid(algorithm, grid, start, end):
	run = True
	while run:
		draw(grid)
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

				start_t = time.time()
				algorithm(lambda: draw(grid), grid, start, end)
				end_t = time.time()
				print("run time: ", end_t - start_t)

	# pygame.quit()
