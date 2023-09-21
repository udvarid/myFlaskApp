from worm import State, Worm, Coordinate, Worm_colour, Worm_dto


class WormBrain:
    def __init__(self):
        self.running = False
        self.size = 0
        self.worms = []

    def run_check(self):
        return self.running

    def run_simulation(self, params):
        self.running = True
        self.size = params.get('size')
        body_types_blue = params.get('worm_blue').get('body_type')
        body_types_red = params.get('worm_red').get('body_type')
        new_worm_blue = Worm(Coordinate(10, 10), body_types_blue, Worm_colour.BLUE, self, map_max=self.size)
        new_worm_red = Worm(Coordinate(30, 30), body_types_red, Worm_colour.RED, self, map_max=self.size)
        self.worms.append(new_worm_blue)
        self.worms.append(new_worm_red)        
        print(f"Starting Simulation, size is {self.size}")

    def stop_simulation(self):
        self.running = False
        self.worms = []
        print("Stopping simulation")

    def ask_next_result(self):
        for worm in self.worms:
            worm.next_phase()
        self.handle_attacked_worms_()
        self.kill_brainless_worms_()
        self.kill_worms_with_only_brain_()
        self.clear_dead_worms_()

        result = self.draw_worm_data()
        # TODO ha az egyik típusú kukacból - darabszám alapon - 90% vagy több van, akkor vége a szimulációnak        
        return result

    def draw_worm_data(self):
        my_array = list()        
        for worm in self.worms:                        
            worm_tdo = worm.build_worm_dto()
            my_array.append(worm_tdo)        
        return my_array

    def handle_attacked_worms_(self):
        for attacked_worm in [x for x in self.worms if x.state == State.ATTACKED]:
            damaged_body_parts = attacked_worm.get_damaged_body_parts()
            if len(damaged_body_parts) > 1:
                attacked_worm.state = State.KILLED
            else:
                damaged_body_part = damaged_body_parts[0]
                index_of_body = [i for i, e in enumerate(attacked_worm.body_parts) if
                                 e.coordinate == damaged_body_part.coordinate][0]
                if index_of_body == 0 or index_of_body == len(attacked_worm.body_parts) - 1:
                    del attacked_worm.body_parts[index_of_body]
                    attacked_worm.state = State.MOVE
                else:
                    self.create_new_worm_(attacked_worm, attacked_worm.body_parts[index_of_body + 1:])
                    attacked_worm.body_parts = attacked_worm.body_parts[:index_of_body]
                    attacked_worm.state = State.MOVE

    def create_new_worm_(self, attacked_worm, body_parts):
        coor = body_parts[0].coordinate
        new_worm = Worm(coor, attacked_worm.body_types_origin, attacked_worm.color, attacked_worm.worm_brain, attacked_worm.map_max)
        new_worm.state = State.REST
        new_worm.body_parts = body_parts
        self.worms.append(new_worm)

    def kill_brainless_worms_(self):
        for worm in self.worms:
            if not worm.worm_has_brain():
                worm.state = State.KILLED

    def kill_worms_with_only_brain_(self):
        for worm in self.worms:
            if worm.state not in [State.EGG, State.BIRTH] and len(worm.get_active_body_parts()) == 1 and worm.worm_has_brain():
                worm.state = State.KILLED

    def clear_dead_worms_(self):
        self.worms = list(filter(lambda x: x.state is not State.KILLED, self.worms))

    def check_way(self, coordinate):
        for worm in self.worms:
            for body_part in worm.body_parts:
                if body_part.coordinate == coordinate:
                    return False
        return True

    def clear_way(self, coordinate):
        for worm in self.worms:
            for body_part in worm.body_parts:
                if body_part.coordinate == coordinate:
                    body_part.damaged = True
                    if worm.state in [State.ATTACKED, State.EGG, State.BIRTH]:
                        worm.state = State.KILLED
                    else:
                        worm.state = State.ATTACKED

    def get_number_of_color_type_worm(self, color):
        return len(list(filter(lambda x: x.color == color, self.worms)))