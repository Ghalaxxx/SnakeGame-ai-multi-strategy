from collections import deque

class SafeAStarPathfinder:
    def __init__(self, grid_width, grid_height, cell_size):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start, goal, obstacles):
        open_list = [start]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            current = min(open_list, key=lambda n: f_score.get(n, float('inf')))

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            open_list.remove(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in obstacles:
                    continue
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    if neighbor not in open_list:
                        open_list.append(neighbor)

        return []

    def bfs_area(self, start, obstacles):
        visited = set()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current in visited or current in obstacles:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in obstacles:
                    queue.append(neighbor)
        return visited

    def find_safe_path(self, start, goal, obstacles, required_space):
        path = self.find_path(start, goal, obstacles)
        if not path:
            return []

        new_head = goal
        new_obstacles = obstacles.copy()
        new_obstacles.add(start)

        reachable_after = self.bfs_area(new_head, new_obstacles)

        if len(reachable_after) >= required_space:
            return path
        else:
            return []
