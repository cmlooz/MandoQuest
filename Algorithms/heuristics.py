import math

def Heuristic(goal, curr_node, has_ship, world, max_ship_fuel):
    cell = world[curr_node[0]][curr_node[1]]
    #Distancia de Manhattan
    heu = abs(curr_node[0] - goal[0]) + abs(curr_node[1] - goal[1])
    # Si tiene la nave, reducimos el costo de movimiento a la mitad
    if 0 < has_ship <= max_ship_fuel:
        heu *= 0.5
    else:
        # Si estamos en una casilla donde hay un enemigo, incrementamos el costo
        if cell == 4:
            heu += 4
    #return 0 if cell == 5 else heu
    return heu

def Heuristic_altern(goal, curr_node, has_ship, world, max_ship_fuel):
    cell = world[curr_node[0]][curr_node[1]]
    #Línea recta
    heu = math.sqrt(((goal[0] - curr_node[0])**2) + ((goal[1] - curr_node[1])**2))
    # Si tiene la nave, reducimos el costo de movimiento a la mitad
    if 0 < has_ship <= max_ship_fuel:
        heu *= 0.5
    else:
        # Si estamos en una casilla donde hay un enemigo, incrementamos el costo
        if cell == 4:
            heu += 4
    #return 0 if cell == 5 else heu
    return heu
