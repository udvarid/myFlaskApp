from enum import Enum
import random


class State(Enum):
    EGG = 1
    BIRTH = 2
    MOVE = 3
    TURN = 4
    EGG_LAYING = 5
    ATTACKED = 6
    KILLED = 7
    REST = 8


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class BodyType(Enum):
    BRAIN = 1
    MOUTH = 2
    LEG = 3
    MULTIPLIER = 4


class Worm_colour(Enum):
    RED = 1,
    BLUE = 2


class Body_part:
    def __init__(self, body_type, coordinate, direction):
        self.body_type = body_type
        self.coordinate = coordinate
        self.born = False
        self.damaged = False
        self.direction = direction

    def create_dto(self):
        return {
            'body_type': get_body_type_dto(self.body_type),
            'coor_x': self.coordinate.x,
            'coor_y': self.coordinate.y,
            'born': self.born,
            'direction': get_direction_dto(self.direction)
        }


class Worm_dto:
    def __init__(self, worm):
        self.color = 'red' if worm.color == Worm_colour.RED else 'blue'
        self.state = 'Egg' if worm.state == State.EGG else 'Live'
        self.direction = get_direction_dto(worm.direction)
        self.coor_x = int(worm.coordinate.x)
        self.coor_y = int(worm.coordinate.y)
        self.bodies = []
        for active_body in worm.get_active_body_parts():
            self.bodies.append(active_body.create_dto())
        unborn_bodies = worm.get_unborn_body_parts()
        if len(unborn_bodies) > 0:
            self.bodies.append(unborn_bodies[0].create_dto())

def get_body_type_dto(body_type):
    if body_type ==  BodyType.BRAIN:
        return 'B'
    elif body_type == BodyType.LEG:
        return 'L'
    elif body_type == BodyType.MOUTH:
        return 'M'
    elif body_type == BodyType.MULTIPLIER:
        return 'X'
    else:
        return ''

def get_direction_dto(direction):        
    worm_direction = ''
    if (direction == Direction.NORTH):
        worm_direction = 'N'
    elif (direction == Direction.SOUTH):
        worm_direction = 'S'
    elif (direction == Direction.EAST):
        worm_direction = 'E'
    elif (direction == Direction.WEST):
        worm_direction = 'W'
    return worm_direction


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Coordinate):
            return (self.x == o.x) and (self.y == o.y)
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Worm:
    def __init__(self, coordinate, body_types, color, worm_brain, map_max):
        self.coordinate = coordinate        
        self.color = color
        self.direction = Direction(random.randint(1, 4))
        self.body_parts = list(map(self.create_body_part, body_types))
        self.body_types_origin = body_types
        self.state = State.EGG
        self.puppeteer_time = 5 + random.randint(1, 5)
        self.move_fragment = self.get_weight()
        self.birth_rest = 0
        self.birth_rest_limit = 10
        self.make_birth = 0.25
        self.change_direction = 0.25
        self.weight = self.get_weight()
        self.map_max = map_max
        self.worm_brain = worm_brain
        self.rest_time = 3

    def build_worm_dto(self):
        return Worm_dto(self)


    def next_phase(self):
        if self.birth_rest > 0:
            self.birth_rest = max(self.birth_rest - len(self.get_multipliers()), 0)
        if self.state == State.EGG:
            self.process_egg_phase()
        elif self.state == State.BIRTH:
            self.process_birth_phase()
        elif self.state == State.MOVE:
            self.process_move_phase()
        elif self.state == State.TURN:
            self.process_turn_phase()
        elif self.state == State.EGG_LAYING:
            self.process_egg_laying_phase()
        elif self.state == State.REST:
            self.process_rest_phase()

    def process_rest_phase(self):
        if self.rest_time > 0:
            self.rest_time = self.rest_time - 1
        else:
            self.state = State.MOVE

    def process_egg_phase(self):
        if self.puppeteer_time > 0:
            self.puppeteer_time = self.puppeteer_time - 1
        else:
            self.state = State.BIRTH

    def process_birth_phase(self):
        next_coordinate = self.get_next_coordinate()
        is_way_free = self.worm_brain.check_way(next_coordinate)
        if self.body_parts[0].body_type == BodyType.MOUTH or is_way_free:
            if not is_way_free:
                self.worm_brain.clear_way(next_coordinate)
            self.coordinate = next_coordinate
            for body_part in self.body_parts:
                past_coordinate = body_part.coordinate
                body_part.coordinate = next_coordinate
                next_coordinate = past_coordinate
                if not body_part.born:
                    body_part.born = True
                    break
            if self.worm_total_born():
                self.state = State.MOVE

    def process_move_phase(self):
        if self.birth_rest == 0 and len(self.get_multipliers()) > 0 and random.random() <= self.make_birth:
            self.state = State.EGG_LAYING
            self.process_egg_laying_phase()
        elif random.random() <= self.change_direction:
            self.state = State.TURN
            self.direction = self.get_new_direction()
            self.process_turn_phase()
        else:
            self.make_move()

    def get_new_direction(self):
        if self.direction in [Direction.EAST, Direction.WEST]:
            return random.choice([Direction.NORTH, Direction.SOUTH])
        else:
            return random.choice([Direction.EAST, Direction.WEST])

    def make_move(self):
        self.weight = max(self.weight - self.get_move(), 0)
        if self.weight == 0:
            next_coordinate = self.get_next_coordinate()
            direction = self.direction
            is_way_free = self.worm_brain.check_way(next_coordinate)
            if self.body_parts[0].body_type == BodyType.MOUTH or is_way_free:
                if not is_way_free:
                    self.worm_brain.clear_way(next_coordinate)
                self.coordinate = next_coordinate
                for body_part in self.body_parts:
                    past_direction = body_part.direction
                    past_coordinate = body_part.coordinate
                    body_part.coordinate = next_coordinate
                    next_coordinate = past_coordinate
                    body_part.direction = direction
                    direction = past_direction
                self.weight = self.get_weight()

    def process_turn_phase(self):
        self.make_move()
        if len(self.get_unturned_body_parts()) == 0:
            self.state = State.MOVE

    def process_egg_laying_phase(self):
        free_places = list(filter(self.worm_brain.check_way, self.get_possible_egg_places()))
        if len(free_places) > 0:
            egg_place = random.choice(free_places)
            new_worm = Worm(egg_place, self.body_types_origin, self.color, self.worm_brain, self.map_max)
            self.worm_brain.worms.append(new_worm)
        self.state = State.MOVE
        self.birth_rest = self.birth_rest_limit

    def get_possible_egg_places(self):
        result = []
        multipliers = list(map(lambda z: z.coordinate, self.get_multipliers()))
        for multiplier in multipliers:
            result.append(Coordinate(multiplier.x-1, multiplier.y-1))
            result.append(Coordinate(multiplier.x,   multiplier.y-1))
            result.append(Coordinate(multiplier.x+1, multiplier.y-1))
            result.append(Coordinate(multiplier.x-1, multiplier.y))
            result.append(Coordinate(multiplier.x+1, multiplier.y))
            result.append(Coordinate(multiplier.x-1, multiplier.y+1))
            result.append(Coordinate(multiplier.x,   multiplier.y+1))
            result.append(Coordinate(multiplier.x+1, multiplier.y+1))
        return list(set(map(self.normalise_coordinate, result)))

    def get_next_coordinate(self):
        new_coordinate = Coordinate(self.coordinate.x, self.coordinate.y)
        if self.direction == Direction.NORTH:
            new_coordinate.y = new_coordinate.y - 1
        elif self.direction == Direction.SOUTH:
            new_coordinate.y = new_coordinate.y + 1
        elif self.direction == Direction.WEST:
            new_coordinate.x = new_coordinate.x - 1
        elif self.direction == Direction.EAST:
            new_coordinate.x = new_coordinate.x + 1
        new_coordinate = self.normalise_coordinate(new_coordinate)
        return new_coordinate

    def create_body_part(self, body_type):
        return Body_part(body_type, self.coordinate, self.direction)

    def get_move(self):
        return len(list(filter(lambda x: x.body_type == BodyType.LEG, self.body_parts))) * 4

    def get_weight(self):
        return sum(map(get_body_part_weight, self.body_parts))

    def get_multipliers(self):
        return list(filter(lambda x: x.body_type == BodyType.MULTIPLIER, self.body_parts))

    def worm_has_brain(self):
        return len(list(filter(lambda x: x.body_type == BodyType.BRAIN, self.body_parts))) > 0

    def worm_total_born(self):
        return len(list(filter(lambda x: x.born is False, self.body_parts))) == 0

    def get_active_body_parts(self):
        return list(filter(lambda x: x.born is True, self.body_parts))

    def get_unborn_body_parts(self):
        return list(filter(lambda x: x.born is False, self.body_parts))

    def get_damaged_body_parts(self):
        return list(filter(lambda x: x.damaged is True, self.body_parts))

    def get_unturned_body_parts(self):
        return list(filter(lambda x: x.direction != self.direction, self.body_parts))

    def normalise_coordinate(self, coordinate):
        result = Coordinate(coordinate.x, coordinate.y)
        if result.x < 1:
            result.x = self.map_max
        elif result.x > self.map_max:
            result.x = 1

        if result.y < 1:
            result.y = self.map_max
        elif result.y > self.map_max:
            result.y = 1
        return result


def get_body_part_weight(body_part):
    if body_part.body_type == BodyType.LEG:
        return 0
    elif body_part.body_type == BodyType.BRAIN:
        return 2
    elif body_part.body_type == BodyType.MOUTH:
        return 1
    elif body_part.body_type == BodyType.MULTIPLIER:
        return 2
    else:
        return 0