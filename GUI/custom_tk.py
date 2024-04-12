import tkinter as tk
from tkinter import ttk, messagebox
import time
from PIL import Image, ImageDraw, ImageFont, ImageTk
from Algorithms import breadth, uniform_cost, depth, avara, a_star
import os

class CustomTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.execution = None
        self.search_results = None
        self.path = None
        self.result = None
        self.title("Mandalorian Quest")
        self.geometry("1100x700")
        self.world = None
        self.start = None
        self.goal = None
        self.max_ship_fuel=0
        self.font= ('Roboto',11)

    def set_variables(self, tmp_world,tmp_start,tmp_goal,tmp_max_ship_fuel):
        self.world = tmp_world
        self.start = tmp_start
        self.goal = tmp_goal
        self.max_ship_fuel = tmp_max_ship_fuel

    def show_loading(self, canvas):
        img = Image.open("./GUI/loading.gif")
        img_tk = ImageTk.PhotoImage(img)
        # Draw the image on the canvas
        canvas.delete("all")
        width = 600
        height = 600
        # Calcula la posición central del panel
        x = (width // 2) - (img.width // 2)
        y = (height // 2) - (img.height // 2)
        canvas.create_image(x, y, image=img_tk, anchor=tk.CENTER)
        canvas.img_tk = img_tk
        self.update_idletasks()

    def hide_loading(self,canvas):
        canvas.delete("all")
        canvas.img_tk = None
        self.update_idletasks()

    def show_type_selector(self):
        self.type_selector.pack()
        self.update_idletasks()

    def hide_type_selector(self):
        self.type_selector.pack_forget()
        self.update_idletasks()

    def show_algorithm_selector(self):
        self.selected_algorithm.pack()
        self.update_idletasks()

    def hide_algorithm_selector(self):
        self.selected_algorithm.pack_forget()
        self.update_idletasks()

    def show_execute_button(self):
        self.execute_button.pack()
        self.update_idletasks()

    def hide_execute_button(self):
        self.execute_button.pack_forget()
        self.update_idletasks()

    def show_results_panel(self):
        self.result.pack()
        self.update_idletasks()

    def hide_results_panel(self):
        self.result.pack_forget()
        self.update_idletasks()

    def show_execution_panel(self):
        self.execution.pack()
        self.update_idletasks()

    def hide_execution_panel(self):
        self.execution.pack_forget()
        self.update_idletasks()

    def show_world(self, curr_world, canvas, has_ship):
        #self.show_loading(canvas)
        #Agregar cuadricula externa
        tmp_world = []
        tmp_row = []
        tmp_row.append("")
        for i,column in enumerate(curr_world[0]):
            tmp_row.append(i)
        tmp_world.append(tmp_row)
        for i,row in enumerate(curr_world):
            tmp_row = []
            tmp_row.append(i)
            for tmp_char in row:
                tmp_row.append(tmp_char)
            tmp_world.append(tmp_row)

        curr_world = tmp_world

        cell_size = 50
        margin = 2
        font_size = cell_size / (margin * 2)
        width = len(curr_world[0]) * cell_size + margin
        height = len(curr_world) * cell_size + margin

        # Create an image object
        img = Image.new("RGB", (width, height), "white")

        # Create a drawing context for the image
        draw = ImageDraw.Draw(img)

        # Create a font object for the numbers
        font = ImageFont.truetype("arial.ttf", font_size)

        # Draw the frame and grid lines on the image
        draw.rectangle([(0, 0), (width, height)], outline="black")
        for i in range(0, width, cell_size):
            draw.line([(i, 0), (i, height)], fill="black")
        for i in range(0, height, cell_size):
            draw.line([(0, i), (width, i)], fill="black")

        # Draw the numbers and colors on the image
        for i, row in enumerate(curr_world):
            for j, cell in enumerate(row):
                x = j * cell_size + (margin * 2)
                y = i * cell_size + (margin * 2)

                #if i == 0 or j == 0:
                #    color = "white"
                #else:
                #    color = {0: "yellow",  1: "gray", 2: "purple", 3: "lightblue", 4: "red", 5: "green"}[cell]

                draw.rectangle([(x, y), (x + (cell_size - (margin * 2)), y + (cell_size - (margin * 2)))])

                if i == 0 or j == 0:
                    draw.text((x + font_size, y + font_size), f"{cell}", fill="black", font=font)
                else:
                    cell = 3 if cell == 2 and 0 < has_ship <= self.max_ship_fuel else cell
                    img_path = {0: "path.jpg", 1: "wall.jpg", 2: "mando.jpg", 3: "razor_crest.jpg", 4: "stormtrooper.jpg",
                     5: "grogu.jpg"}[cell]

                    cell_img = Image.open("./GUI/" + img_path)
                    cell_img = cell_img.resize(
                        (cell_size - 1 * margin, cell_size - 1 * margin))  # Resize image to fit cell
                    img.paste(cell_img, (x + margin, y + margin))  # Paste image onto cell


        #self.hide_loading(canvas)

        # Convert the image to a Tkinter-compatible photo image
        img_tk = ImageTk.PhotoImage(img)

        # Draw the image on the canvas
        canvas.delete("all")
        canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)

        # Keep a reference to the photo image to prevent it from being garbage collected
        canvas.img_tk = img_tk

    def old_create_widgets(self):
        # Set the background color for the whole application
        self.configure(bg='white')

        # Create the "Config" frame
        self.config_frame = tk.Frame(self, width=180, height=600)
        self.config_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Create the "world" frame
        self.world_frame = tk.Frame(self, width=600, height=600)
        self.world_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        # Create a canvas widget in the "world" frame
        self.canvas = tk.Canvas(self.world_frame, width=600, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Create the "selectors" frame
        self.selectors_frame = tk.Frame(self.config_frame, width=200, height=200)
        self.selectors_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Create the "Selector de tipo" frame
        self.tipo_frame = tk.Frame(self.selectors_frame, width=80, height=100)
        self.tipo_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a selector widget in the "Selector de tipo" frame
        ttk.Label(self.tipo_frame, text="Tipo de búsqueda").pack()  # Añade un label
        self.type_selector = ttk.Combobox(self.tipo_frame, values=["No informada", "Informada"], state="readonly")
        self.type_selector.bind("<<ComboboxSelected>>", self.update_algorithms)  # Vincula el evento de cambio
        self.type_selector.pack()

        # Create the "Selector de algorithm" frame
        self.algorithm_frame = tk.Frame(self.selectors_frame, width=80, height=100)
        self.algorithm_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a selector widget in the "Selector de algorithm" frame
        ttk.Label(self.algorithm_frame, text="Algorítmo").pack()  # Añade un label
        self.selected_algorithm = ttk.Combobox(self.algorithm_frame, state="readonly")
        self.selected_algorithm.bind("<<ComboboxSelected>>", self.update_execution_button)  # Vincula el evento de cambio
        self.selected_algorithm.pack()

        # Create the "Button" frame
        self.button_frame = tk.Frame(self.config_frame, width=200, height=100)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Create the "Ejecutar" button
        self.execute_button = tk.Button(self.button_frame, text="Ejecutar",
                                         command=lambda: self.search(
                                             algorithm=self.selected_algorithm.get()))
        #self.execute_button.pack()

        # Create the "result" frame
        self.result_frame = tk.Frame(self.config_frame, width=200, height=200)
        self.result_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.result = ttk.Label(self.result_frame, text="result")
        # self.result.pack()

        # Create the "execution" frame
        self.execution_frame = tk.Frame(self.config_frame, width=200, height=200)
        self.execution_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
        # Create the "execution" frame
        self.execution = ttk.Label(self.execution_frame, text="execution")
        # self.execution.pack()

    def create_widgets(self):
        # Set the background color for the whole application
        self.configure(bg='white')

        # Create the "Config" frame
        self.config_frame = tk.Frame(self, width=180, height=600, bg='white')
        self.config_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Create the "world" frame
        self.world_frame = tk.Frame(self, width=600, height=600, bg='white')
        self.world_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        # Create a canvas widget in the "world" frame
        self.canvas = tk.Canvas(self.world_frame, width=600, height=600, bg='white')
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Create the "selectors" frame
        self.selectors_frame = tk.Frame(self.config_frame, width=200, height=200,bg='white')
        self.selectors_frame.pack(side=tk.TOP, padx=10, pady=10)


        # Create the "Selector de tipo" frame
        self.tipo_frame = tk.Frame(self.selectors_frame, width=80, height=100, bg='white')
        self.tipo_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a selector widget in the "Selector de tipo" frame
        ttk.Label(self.tipo_frame, text="Tipo de búsqueda", font=self.font).pack()  # Añade un label
        self.type_selector = ttk.Combobox(self.tipo_frame, values=["No informada", "Informada"], state="readonly",
                                          font=self.font)
        self.type_selector.bind("<<ComboboxSelected>>", self.update_algorithms)  # Vincula el evento de cambio
        self.type_selector.pack(fill=tk.X)

        # Create the "Selector de algorithm" frame
        self.algorithm_frame = tk.Frame(self.selectors_frame, width=80, height=100, bg='white')
        self.algorithm_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a selector widget in the "Selector de algorithm" frame
        ttk.Label(self.algorithm_frame, text="Algorítmo", font=self.font).pack()  # Añade un label
        self.selected_algorithm = ttk.Combobox(self.algorithm_frame, state="readonly", font=self.font)
        self.selected_algorithm.bind("<<ComboboxSelected>>",
                                     self.update_execution_button)  # Vincula el evento de cambio
        self.selected_algorithm.pack(fill=tk.X)

        # Create the "Button" frame
        self.button_frame = tk.Frame(self.config_frame, width=200, height=100, bg='white')
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Create the "Ejecutar" button
        self.execute_button = tk.Button(self.button_frame, text="Ejecutar",
                                        font=self.font, bg='green', fg='white',
                                        command=lambda: self.search(algorithm=self.selected_algorithm.get()))
        #self.execute_button.pack(fill=tk.X)

        # Create the "rounded border" style
        style = ttk.Style()
        style.configure('TButton',
                        foreground='white',
                        background='green',
                        font=self.font,
                        borderwidth=2,
                        padding=6,
                        relief='groove')

        # Create the "result" frame
        self.result_frame = tk.Frame(self.config_frame, width=200, height=200, bg='white')
        self.result_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.result = ttk.Label(self.result_frame, text='result')
        # self.result.pack()

        # Create the "execution" frame
        self.execution_frame = tk.Frame(self.config_frame, width=200, height=200, bg='white')
        self.execution_frame.pack(side=tk.TOP, padx=10, pady=10)
        # Create the "execution" frame
        self.execution = ttk.Label(self.execution_frame, text='execution')
        # self.execution.pack()

    def update_algorithms(self, event=None):
        if self.type_selector.get() == "No informada":
            algorithms = ["Amplitud", "Costo Uniforme", "Profundidad"]
        else:
            algorithms = ["Avara", "A*"]

        self.selected_algorithm.config(values=algorithms)

    def update_execution_button(self, event=None):
        if self.selected_algorithm.get() is not None and self.selected_algorithm.get() != "":
            self.show_execute_button()
        else:
            self.hide_execute_button()

    def update_results(self, algorithm, expanded_nodes, tree_depth, process_time, solution_cost=None):
        report = f"Algorítmo seleccionado: {algorithm}\n"
        report += f"Inicio: ({self.start[0]},{self.start[1]}), Meta: ({self.goal[0]},{self.goal[1]})\n"
        report += f"Cantidad de nodes expandidos: {expanded_nodes}\n"
        report += f"Profundidad del árbol: {tree_depth}\n"
        report += f"time de cómputo: {process_time:.2f} segundos\n"
        if solution_cost:
            report += f"Costo de la solución encontrada: {solution_cost}\n"
        #messagebox.showinfo("report ejecución", report)
        self.show_results_panel()
        self.result.config(text=report)

    def update_execution(self, curr_node):
        report = f"Posición actual: ({curr_node.action[0]},{curr_node.action[1]})\n"
        report += f"Costo acumulado: {curr_node.current_cost}\n"
        report += f"Profundidad del nodo: {curr_node.depth}\n"
        report += f"Heurística: {curr_node.heuristic}\n"
        report += f"Lleva nave: { curr_node.has_ship }\n"
        self.execution.config(text=report)
        self.show_execution_panel()

    def search(self, algorithm):
        self.show_world(curr_world=self.world,canvas=self.canvas, has_ship=0)
        self.show_loading(self.canvas)
        self.hide_results_panel()
        self.hide_execution_panel()
        self.result.config(text="")
        self.execution.config(text="")
        self.hide_type_selector()
        self.hide_algorithm_selector()
        self.hide_execute_button()
        self.search_results = None
        self.path = None
        start_time = time.time()

        if algorithm is None or algorithm == "":
            self.hide_loading(self.canvas)
            messagebox.showinfo("Error de ejecución", "No se ha seleccionado el algorítmo")
            #return False

        if algorithm == 'Amplitud':
            self.search_results = breadth.Breadth(self.world, self.start, self.goal, self.max_ship_fuel)
        elif algorithm == 'Costo Uniforme':
            self.search_results = uniform_cost.UniformCost(self.world, self.start, self.goal, self.max_ship_fuel)
        elif algorithm == 'Profundidad':
            self.search_results = depth.Depth(self.world, self.start, self.goal, self.max_ship_fuel)
        elif algorithm == 'Avara':
            self.search_results = avara.Avara(self.world, self.start, self.goal, self.max_ship_fuel)
        elif algorithm == 'A*':
            self.search_results = a_star.AStar(self.world, self.start, self.goal, self.max_ship_fuel)
        else:
            self.hide_loading(self.canvas)
            raise ValueError(f"Unknown algorithm: {algorithm}")

        self.path = self.search_results.execute()
        self.search_results.process_time = time.time() - start_time
        self.hide_loading(self.canvas)
        self.update_results(algorithm=algorithm, expanded_nodes=self.search_results.expanded_nodes,
                            tree_depth=self.search_results.tree_depth, process_time=self.search_results.process_time,
                            solution_cost=self.search_results.solution_cost)
        if self.path:
            for curr_node in self.path:
                self.show_world(curr_world=curr_node.state, canvas=self.canvas,has_ship=curr_node.has_ship)
                self.update_execution(curr_node)
                self.update_idletasks()
                time.sleep(0.75)

        self.show_type_selector()
        self.show_algorithm_selector()
        self.hide_execution_panel()
        self.execution.config(text="")
