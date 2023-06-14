from copy import deepcopy
from random import randint


class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cell):
            return (self.x == o.x) and (self.y == o.y) and (self.value == o.value)
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.value))


class GameOfLifeBrain:

    def __init__(self):
        self.running = False
        self.size = 100
        self.players = 1
        self.init_cells = 10
        self.universe = set()
        self.firstRound = True
        self.init_array = []

    def run_check(self):
        return self.running

    def run_simulation(self, params):
        self.running = True
        self.firstRound = True
        self.size = params.get('size', 50)
        self.players = params.get('players', 1)
        self.init_cells = params.get('init_cells', 10)
        self.init_array = self.get_empty_array()
        print(
            f"Starting Simulation, size is {self.size}, "
            f"number of players is {self.players}, init cells is {self.init_cells}")
        self.place_init_cells()

    def stop_simulation(self):
        self.running = False
        self.universe = set()
        print("Stopping simulation")

    def ask_next_result(self):
        print('Giving result')
        result = self.calculate_next_step()
        return result

    def place_init_cells(self):
        for i in range(self.players):
            center_x = self.size / 4
            center_y = self.size / 4
            if i == 1:
                center_x = self.size / 4 * 3
            elif i == 2:
                center_y = self.size / 4 * 3
            elif i == 3:
                center_x = self.size / 4 * 3
                center_y = self.size / 4 * 3
            self.place_random_cells_around_center(center_x, center_y, i + 1)

    def place_random_cells_around_center(self, x, y, tribe):
        while not self.tribe_is_ready(tribe):
            rand_x = 9 - randint(0, 18)
            rand_y = 9 - randint(0, 18)
            cell = Cell(x + rand_x, y + rand_y, tribe)
            self.universe.add(cell)

    def tribe_is_ready(self, tribe):
        return len(list(filter(lambda cell: cell.value == tribe, self.universe))) >= self.init_cells

    def calculate_next_step(self):
        empty_neighbour_cells = self.get_empty_neighbours()
        final_empty_neighbour_cells = set()
        for empty in empty_neighbour_cells:
            if self.cell_has_place(empty):
                final_empty_neighbour_cells.add(empty)
        cells_to_calculate = set()
        cells_to_calculate.update(final_empty_neighbour_cells)
        cells_to_calculate.update(self.universe)
        if self.firstRound:
            next_version = self.universe
            self.firstRound = False
        else:
            next_version = get_next_version(cells_to_calculate)
        self.universe = next_version
        my_array = deepcopy(self.init_array)
        for cell in next_version:            
            my_array[int(cell.x)][int(cell.y)] = int(cell.value)        
        return next_version

    def cell_has_place(self, empty):
        for cell in self.universe:
            if cell.x == empty.x and cell.y == empty.y:
                return False
        return True

    def get_empty_neighbours(self):
        empties = set()
        for cell in self.universe:
            empties.update(self.get_empty_neighbours_for_given_cell(cell))
        return empties

    def get_empty_neighbours_for_given_cell(self, cell):
        empties = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0) and 0 <= cell.x + i < self.size and 0 <= cell.y + j < self.size:
                    empties.add(Cell(cell.x + i, cell.y + j, 0))
        return empties

    def get_empty_array(self):
        my_array = []
        n = self.size
        for i in range(n):
            my_row = []
            for j in range(n):
                my_row.append(0)
            my_array.append(my_row)
        return my_array


def get_next_version(cells):
    final_cells = set()
    dead_cells = list(filter(lambda cell: cell.value == 0, cells))
    living_cells = list(filter(lambda cell: cell.value != 0, cells))
    for dead_cell in dead_cells:
        neighbouring_living_cells_next_to_dead_cell = get_neighbouring_living_cells(living_cells, dead_cell)
        if len(neighbouring_living_cells_next_to_dead_cell) == 3 and cells_from_same_tribe(
                neighbouring_living_cells_next_to_dead_cell):
            dead_cell.value = list(neighbouring_living_cells_next_to_dead_cell)[0].value
            final_cells.add(dead_cell)

    for living_cell in living_cells:
        neighbouring_living_cells = get_neighbouring_living_cells(living_cells, living_cell)
        if 2 <= len(neighbouring_living_cells) <= 3:
            final_cells.add(living_cell)
    return final_cells


def cells_from_same_tribe(cells):
    if len(cells) > 0:
        tribe = list(cells)[0].value
        for cell in cells:
            if cell.value != tribe:
                return False
    return True


def get_neighbouring_living_cells(cells, living_cell):
    neighbouring_living_cells = set()
    for cell in cells:
        if cell != living_cell and \
                abs(cell.x - living_cell.x) <= 1 and \
                abs(cell.y - living_cell.y) <= 1:
            neighbouring_living_cells.add(cell)
    return neighbouring_living_cells
