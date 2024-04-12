from Algorithms import heuristics

def read_file(curr_file_name):
    curr_world = []
    with open(curr_file_name, 'r') as file:
        for line in file:
            row = [int(value) for value in line.strip().split()]
            curr_world.append(row)
    return curr_world

def get_start_goal(curr_world):
    tmp_start = None
    tmp_goal = None

    for row in curr_world:
        for tmp_char in row:
            if tmp_char == 2:
                tmp_start = ((curr_world.index(row)), row.index(tmp_char))
            elif tmp_char == 5:
                tmp_goal = ((curr_world.index(row)), row.index(tmp_char))
    return  tmp_start, tmp_goal

def write_to_file(file_, text):
    with open(file_, "a") as file:
        file.write(text + "\n")

if __name__ == '__main__':
    #app.show_loading(canvas=app.canvas)
    file_name = 'Prueba2.txt'
    max_ship_fuel = 10
    world = read_file(file_name)
    start, goal = get_start_goal(world)

    list_nodes = [(0, 3), (2, 6), (2, 9), (8, 9), (9, 9), (9, 8)]

    #list_nodes.append((4,6))

    filename = "result.txt"

    # Itera sobre los nodos y escribe los resultados en el archivo
    for curr_node in list_nodes:
        write_to_file(filename, f"Posicion: ({curr_node[0]},{curr_node[1]})")
        write_to_file(filename,
                      "Heuristica sin nave: " + str(heuristics.Heuristic(goal, curr_node, 0, world, max_ship_fuel)))
        write_to_file(filename, "____________")

    for curr_node in list_nodes:
        write_to_file(filename, f"Posicion: ({curr_node[0]},{curr_node[1]})")
        write_to_file(filename,
                      "Heuristica con nave: " + str(heuristics.Heuristic(goal, curr_node, 1, world, max_ship_fuel)))
        write_to_file(filename, "____________")

    write_to_file(filename, "**********")

    for curr_node in list_nodes:
        write_to_file(filename, f"Posicion: ({curr_node[0]},{curr_node[1]})")
        write_to_file(filename,
                      "Heuristic_altern sin nave: " + str(heuristics.Heuristic_altern(goal, curr_node, 0, world, max_ship_fuel)))
        write_to_file(filename, "____________")

    for curr_node in list_nodes:
        write_to_file(filename, f"Posicion: ({curr_node[0]},{curr_node[1]})")
        write_to_file(filename,
                      "Heuristic_altern con nave: " + str(heuristics.Heuristic_altern(goal, curr_node, 1, world, max_ship_fuel)))
        write_to_file(filename, "____________")