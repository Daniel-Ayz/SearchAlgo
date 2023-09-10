# SearchAlgo
def algorithm1(draw, grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0

    while open_set:
        if is_terminated():
            return False

        current_distance, current = heapq.heappop(open_set)

        if current == end:
            draw()
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor.is_closed():
                continue
            tentative_distance = distance[current] + 1

            if tentative_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = tentative_distance
                heapq.heappush(open_set, (distance[neighbor], neighbor))
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
