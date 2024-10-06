import heapq
import algorithm
import settings

# Constants for movement costs
ORTHOGONAL_COST = 10
DIAGONAL_COST = 14

class AStar(algorithm.VisualisableAlgorithm):
    def __init__(self, app, pos_start, pos_end, wall_pos):
        super().__init__(app, pos_start, pos_end, wall_pos)
        self.open_list = []
        self.closed_list = set()
        self.route = []
        self.route_found = False

    def execute(self):
        # Initialize Start/End Nodes
        start_node = Node(self.pos_start, None)
        end_node = Node(self.pos_end, None)

        heapq.heappush(self.open_list, (start_node.F, start_node))

        while self.open_list:
            current_node = heapq.heappop(self.open_list)[1]

            if self.find_end(current_node.position):
                self.construct_route(current_node)
                self.route_found = True
                break

            self.generate_children(current_node, end_node)
            self.draw_all_paths(current_node.position, settings.TAN)

            self.closed_list.add(current_node.position)

    def construct_route(self, current_node):
        while current_node:
            self.route.append(current_node.position)
            current_node = current_node.parent
        self.route.reverse()

    def get_routes(self):
        return [self.route]

    def is_valid(self, position):
        return position not in self.wall_pos and position not in self.closed_list

    def find_end(self, current):
        return current == self.pos_end

    def generate_children(self, parent, end_node):
        parent_pos = parent.position
        for move in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            child_pos = (parent_pos[0] + move[0], parent_pos[1] + move[1])
            if self.is_valid(child_pos):
                child = Node(child_pos, parent)
                self.calc_g(child, parent, move)
                self.calc_h(child, end_node)
                self.calc_f(child)

                if self.append_to_open(child) and self.check_wall_corner(move, parent_pos):
                    heapq.heappush(self.open_list, (child.F, child))

    def append_to_open(self, child):
        for _, open_node in self.open_list:
            if child.position == open_node.position and child.F >= open_node.F:
                return False
        return True

    def check_wall_corner(self, move, parent_pos):
        if move in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
            i, j = parent_pos
            (m, n) = move
            orthogonal_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for orthogonal in orthogonal_moves:
                if (i + orthogonal[0], j + orthogonal[1]) in self.wall_pos:
                    return False
            return True
        return True

    def calc_g(self, child, parent, move):
        if abs(sum(move)) == 1:
            child.G = parent.G + ORTHOGONAL_COST
        else:
            child.G = parent.G + DIAGONAL_COST

    def calc_h(self, child, end_node):
        dx = abs(child.position[0] - end_node.position[0])
        dy = abs(child.position[1] - end_node.position[1])
        child.H = ORTHOGONAL_COST * (dx + dy)

    def calc_f(self, child):
        child.F = child.G + child.H


class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent
        self.G = 0
        self.H = 0
        self.F = 0

    def __lt__(self, other):
        return self.F < other.F
