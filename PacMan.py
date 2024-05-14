from GameObject import GameObject
from GameDefs import Pos, SpriteType, Direction, globals
import heapq

class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)

    def move(self):
        start = (self.position.x, self.position.y)
        goal = (globals.pill.position.x, globals.pill.position.y)
        grid = self.make_grid()

        path = astar(start, goal, grid)
        

        if path:
            next_position = path[1]  # Next position after the current position
            dx = next_position[0] - self.position.x
            dy = next_position[1] - self.position.y

            if dx == 1:
                return Direction.RIGHT
            elif dx == -1:
                return Direction.LEFT
            elif dy == 1:
                return Direction.DOWN
            elif dy == -1:
                return Direction.UP
        else:
            return Direction.NONE

    def make_grid(self):
        grid = []
        for i in range(globals.gameSize):
            row = []
            for j in range(globals.gameSize):
                cell_position = (i, j)
                if self.check_position(cell_position) == SpriteType.WALL:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        return grid

    @staticmethod
    def check_position(p):
        for obj in GameObject.gameObjects:
            if obj.position.x == p[0] and obj.position.y == p[1]:
                return obj.type
        return SpriteType.EMPTY

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic cost from current node to goal node
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

def astar(start, goal, grid):
    open_list = []
    closed_set = set()

    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == goal_node.position:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node.position)

        for next_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent positions (up, down, left, right)
            node_position = (current_node.position[0] + next_position[0], current_node.position[1] + next_position[1])

            if node_position[0] < 0 or node_position[0] >= len(grid) or node_position[1] < 0 or node_position[1] >= len(grid[0]):
                continue

            if grid[node_position[0]][node_position[1]] == 1:
                continue

            new_node = Node(node_position, current_node)
            new_node.g = current_node.g + 1
            new_node.h = abs(node_position[0] - goal_node.position[0]) + abs(node_position[1] - goal_node.position[1])
            new_node.f = new_node.g + new_node.h

            if node_position in closed_set:
                continue

            heapq.heappush(open_list, new_node)

    return None  # No path found

#Tree Decisions
def treedecisions(pacman_position, ghost_position, pill_position):
    #Priority 1: Avoid Ghost
    if abs(ghost_position.x - pacman_position.x) <3 and abs(ghost_position.y - pacman_position.y) <3:
        if abs(ghost_position.x - pacman_position.x) > abs(ghost_position.y - pacman_position.y):
            if ghost_position.x > pacman_position.x:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        else:
            if ghost_position.y > pacman_position.y:
                return Direction.UP
            else:
                return Direction.DOWN
    
    return treedecisions(pacman_position, ghost_position, pill_position)
    