import tkinter as tk
import heapq

ROWS, COLS = 10, 10
WALL = '#'
START = 'S'
END = 'E'
PATH = '*'
EMPTY = '.'

city_names_list = [
    'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai',
    'kolkata', 'pune', 'ahmedabad', 'jaipur', 'lucknow'
]

class Node:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.g = float('inf')
        self.h = 0
        self.f = 0
        self.prev = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a.r - b.r) + abs(a.c - b.c)

def get_neighbors(node, nodes, grid):
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = node.r + dr, node.c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if grid[nr][nc] != WALL:
                neighbors.append(nodes[nr][nc])
    return neighbors

def a_star(start, end, nodes, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g = 0
    start.f = heuristic(start, end)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            while current.prev:
                if grid[current.r][current.c] not in (START, END):
                    grid[current.r][current.c] = PATH
                current = current.prev
            return True

        for neighbor in get_neighbors(current, nodes, grid):
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.prev = current
                heapq.heappush(open_set, (neighbor.f, neighbor))

    return False

class QuestionWindow:
    def __init__(self, root, visualization_window):
        self.root = root
        self.visualization_window = visualization_window
        self.root.title("City Navigator - Question Window")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter Start City:").pack(pady=5)
        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack(pady=5)

        tk.Label(self.root, text="Enter End City:").pack(pady=5)
        self.end_entry = tk.Entry(self.root)
        self.end_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Wall Cities (space-separated):").pack(pady=5)
        self.walls_entry = tk.Entry(self.root)
        self.walls_entry.pack(pady=5)

        tk.Button(self.root, text="Start Visualization", command=self.start_visualization).pack(pady=10)

    def start_visualization(self):
        start_input = self.start_entry.get().strip().lower()
        end_input = self.end_entry.get().strip().lower()
        walls_input = self.walls_entry.get().strip().lower().split()

        if start_input not in city_names_list or end_input not in city_names_list:
            print("Invalid city name for start or end.")
            return

        sr = city_names_list.index(start_input)
        er = city_names_list.index(end_input)

        sc = sr  # placing on diagonal
        ec = er

        wall_coords = []
        for city in walls_input:
            if city in city_names_list:
                i = city_names_list.index(city)
                wall_coords.append((i, i))  # diagonal

        self.visualization_window.update_grid(sr, sc, er, ec, wall_coords)
        self.visualization_window.show_grid()

class VisualizationWindow:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        self.cell_size = 60  # Fits 10x10 in 600px
        self.start = None
        self.end = None
        self.walls = set()
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.nodes = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

    def update_grid(self, sr, sc, er, ec, walls):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.nodes = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

        self.start = (sr, sc)
        self.end = (er, ec)
        self.walls = set(walls)

        for r, c in walls:
            self.grid[r][c] = WALL
        self.grid[sr][sc] = START
        self.grid[er][ec] = END

    def show_grid(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                color = "white"
                if self.grid[r][c] == START:
                    color = "green"
                elif self.grid[r][c] == END:
                    color = "red"
                elif self.grid[r][c] == WALL:
                    color = "black"
                elif self.grid[r][c] == PATH:
                    color = "blue"
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color)

        tk.Button(self.root, text="Run A* Algorithm", command=self.run_algorithm).pack(pady=10)

    def run_algorithm(self):
        sr, sc = self.start
        er, ec = self.end

        start_node = self.nodes[sr][sc]
        end_node = self.nodes[er][ec]

        found = a_star(start_node, end_node, self.nodes, self.grid)

        if found:
            print("Path found.")
        else:
            print("No path found.")
        self.show_grid()

def main():
    root1 = tk.Tk()
    root2 = tk.Tk()

    visualization_window = VisualizationWindow(root2)
    question_window = QuestionWindow(root1, visualization_window)

    root1.mainloop()
    root2.mainloop()

if __name__ == "__main__":
    main()
