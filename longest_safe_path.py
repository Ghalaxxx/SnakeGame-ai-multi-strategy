
from collections import deque

class LongestSafePathFinder:
    def __init__(self, grid_width, grid_height, cell_size):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size

    def get_neighbors(self, node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                neighbors.append((nx, ny))
        return neighbors

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

    def dfs_paths(self, start, goal, obstacles, path=None, visited=None, all_paths=None, max_paths=10):
        if path is None:
            path = [start]
        if visited is None:
            visited = set()
        if all_paths is None:
            all_paths = []

        if len(all_paths) >= max_paths:
            return all_paths

        if start == goal:
            all_paths.append(path)
            return all_paths

        visited.add(start)

        if len(path) > 40:
            return all_paths

        for neighbor in self.get_neighbors(start):
            if neighbor not in visited and neighbor not in obstacles:
                self.dfs_paths(neighbor, goal, obstacles, path + [neighbor], visited.copy(), all_paths, max_paths)

        return all_paths

    def find_longest_safe_path(self, start, goal, obstacles, required_space):
        all_paths = self.dfs_paths(start, goal, obstacles, max_paths=10)
        longest_safe = []

        for path in all_paths:
            simulated_head = goal
            simulated_obstacles = obstacles.copy()
            simulated_obstacles.add(start)
            area = self.bfs_area(simulated_head, simulated_obstacles)
            if len(area) >= required_space:
                if len(path) > len(longest_safe):
                    longest_safe = path

        return longest_safe
