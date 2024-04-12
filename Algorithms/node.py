class Node:
    def __init__(self, state, father=None, action=None, current_cost=0, has_ship=0, depth = 0, heuristic=None):
        self.state = state
        self.father = father
        self.action = action
        self.current_cost = current_cost
        self.has_ship = has_ship
        self.depth = depth
        self.heuristic = heuristic
