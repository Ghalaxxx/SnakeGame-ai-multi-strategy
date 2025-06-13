from collections import deque
from astar import AStarPathfinder

class SafeAStarFloodFill(AStarPathfinder):
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

    def find_safe_astar_path(self, start, goal, obstacles, required_space):
        path = self.find_path(start, goal, obstacles)
        if not path:
            return []

        # simulate snake moving to the goal
        simulated_head = goal
        simulated_obstacles = obstacles.copy()
        simulated_obstacles.add(start)

        area = self.bfs_area(simulated_head, simulated_obstacles)
        if len(area) >= required_space:
            return path
        else:
            return []
