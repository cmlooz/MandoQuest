from GUI import custom_tk


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

if __name__ == '__main__':
    app = custom_tk.CustomTk()
    #app.show_loading(canvas=app.canvas)
    file_name = 'Prueba1.txt'
    max_ship_fuel = 10
    world = read_file(file_name)
    start, goal = get_start_goal(world)

    app.set_variables(tmp_world=world, tmp_start=start, tmp_goal=goal, tmp_max_ship_fuel=max_ship_fuel)
    app.create_widgets()
    #app.hide_loading(canvas=app.canvas)
    app.show_world(curr_world=world, canvas=app.canvas, has_ship=0)

    app.mainloop()