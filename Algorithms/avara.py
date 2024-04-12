import heapq
import math

from Algorithms import node, heuristics


class Avara:
    def __init__(self, world, start, goal, max_ship_fuel):
        self.world = world
        self.start = start
        self.goal = goal
        self.expanded_nodes = 0
        self.tree_depth = 0
        self.process_time = 0
        self.solution_cost = 0
        self.max_ship_fuel = max_ship_fuel

    def generated_nodes(self, curr_node):
        generated_nodes = []
        # (0,1) = Abajo
        # (1,0) = Derecha
        # (0,-1) = Arriba
        # (-1,0) = Izquierda
        for action in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            x, y = curr_node.action[0] + action[0], curr_node.action[1] + action[1]
            #Si está dentro de los limites del mundo
            if 0 <= x < len(self.world) and 0 <= y < len(self.world[0]):
                #Si no es un muro
                if self.world[x][y] != 1:
                    old_x, old_y = curr_node.action
                    new_state = [[inner_list for inner_list in sublist] for sublist in curr_node.state]
                    # Poner un 0 para el paso anterior si era la posición actual o la nave, si ya se acabó el combustible de la nave se baja
                    new_state[old_x][old_y] = 0 if self.world[old_x][old_y] == 2 or self.world[old_x][
                        old_y] == 3 else 3 if curr_node.has_ship == self.max_ship_fuel and self.world[old_x][
                        old_y] != 3 else self.world[old_x][old_y]
                    # Posición actual
                    new_state[x][y] = 2
                    new_cost, has_ship = self.current_cost(self.world[x][y], curr_node.current_cost, curr_node.has_ship)
                    has_ship = has_ship if curr_node.has_ship < self.max_ship_fuel + 1 else 0
                    new_node = node.Node(state=new_state, father = curr_node, action = (x, y), current_cost=new_cost, has_ship=has_ship, depth=curr_node.depth + 1, heuristic=self.heuristic(curr_node=(x, y),has_ship=has_ship))
                    #Evitar devolverse
                    if curr_node.father is None or curr_node.father.action != new_node.action or (curr_node.father.action == new_node.action and (curr_node.father.has_ship != new_node.has_ship or curr_node.father.state != new_node.state)):
                        generated_nodes.append(new_node)
        return generated_nodes

    def path(self, curr_node):
        path = []
        while curr_node is not None:
            path.append(curr_node)
            curr_node = curr_node.father

        return path[::-1]

    def current_cost(self,cell, current_cost, has_ship = 0):
        cost = 1
        if cell is None:
            return 0, 0
        else:
            if 0 < has_ship <= self.max_ship_fuel:
                cost = 0.5
                has_ship += 1
            elif cell == 0:
                cost = 1
            elif cell == 4 and (has_ship == 0 or has_ship > self.max_ship_fuel):
                cost = 5
            elif cell == 3 and has_ship < self.max_ship_fuel:
                cost = 0.5
                has_ship += 1
            return (current_cost + cost), has_ship

    def heuristic(self,curr_node, has_ship):
        return heuristics.Heuristic(goal=self.goal, curr_node=curr_node, has_ship=has_ship, world=self.world,
                                    max_ship_fuel=self.max_ship_fuel)
    def print_node(self, curr_node):
        report = f"Posición actual: ({curr_node.action[0]},{curr_node.action[1]})\n"
        report += f"Costo acumulado: {curr_node.current_cost}\n"
        report += f"Profundidad del nodo: {curr_node.depth}\n"
        report += f"Heurística: {curr_node.heuristic}\n"
        report += f"Lleva nave: { curr_node.has_ship }\n"
        report += f"__________________\n"
        print(report)

    def execute(self):
        curr_node = node.Node(state=self.world, father=None, action=self.start, current_cost=0, has_ship=0, depth=0, heuristic=self.heuristic(curr_node=self.start, has_ship=0))
        nodes_queue = CustomPriorityQueue()
        nodes_queue.push(curr_node)

        while not nodes_queue.is_empty():
            curr_node = nodes_queue.pop()
            self.print_node(curr_node)
            self.tree_depth = curr_node.depth
            self.expanded_nodes += 1
            self.solution_cost = curr_node.current_cost
            if curr_node.action == self.goal:
                return self.path(curr_node)

            generated_nodes = self.generated_nodes(curr_node)
            for new_node in generated_nodes:
                nodes_queue.push(new_node)

        return None

class CustomPriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, current_node):
        tmp_node = CustomNode(curr_heuristic=current_node.heuristic, curr_node=current_node)
        heapq.heappush(self.queue, (tmp_node.current_heuristic, tmp_node))

    def pop(self):
        return heapq.heappop(self.queue)[1].current_node

    def is_empty(self):
        return len(self.queue) == 0

class CustomNode:
    def __init__(self, curr_heuristic, curr_node):
        self.current_heuristic = curr_heuristic
        self.current_node = curr_node
    def __lt__(self, other):
        return self.current_heuristic < other.current_heuristic