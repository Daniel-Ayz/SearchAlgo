
import math
import time
from queue import PriorityQueue

from grid.grid_visualizer import Spot, make_grid, get_clicked_pos, validate_click, is_terminated, run_algorithm


def manhattan(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return (abs(x1 - x2) + abs(y1 - y2)) * 1.001


def euclidean(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) * 1.001
	# suboptimal but fast
	# return (x1 - x2)**2 + (y1 - y2)**2


def reconstruct_path(came_from, current, draw):
	count = 0
	while current in came_from:
		count += 1
		current = came_from[current]
		current.make_path()
		draw()
	print(f"path length: {count}")


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = manhattan(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		if is_terminated():
			return False

		current = open_set.get()[2]
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
				f_score[neighbor] = temp_g_score + manhattan(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


if "__main__" == __name__:
	run_algorithm(algorithm)
