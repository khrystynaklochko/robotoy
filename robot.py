import fileinput
from re import compile, X

COMMANDS = {
    'NORTH': {
        'left': 'WEST',
        'right': 'EAST'
    },
    'WEST': {
        'left': 'SOUTH',
        'right': 'NORTH'
    },
    'SOUTH': {
        'left': 'EAST',
        'right': 'WEST'
    },
    'EAST': {
        'left': 'NORTH',
        'right': 'SOUTH'
    },
}

ALLOWED_COMMANDS = compile(
    r"""
        (?P<x>\d+),                 
        (?P<y>\d+),                  
        (?P<d>NORTH|EAST|SOUTH|WEST)
        """, X
)

X_MOVEMENTS = {0, 1, 2, 3, 4}
Y_MOVEMENTS = {0, 1, 2, 3, 4}
D_MOVEMENTS = {'NORTH', 'EAST', 'SOUTH', 'WEST'}

class InvalidCommand(Exception):
    """Invalid command"""
    pass

class InvalidPosition(Exception):
    """AMOUNT EXEEDED"""
    pass

class Position():
    _x = None
    _y = None
    _d = None

    def __init__(self, current_position):
        if current_position['x'] in X_MOVEMENTS and current_position['y'] in Y_MOVEMENTS and current_position['d'] in D_MOVEMENTS:
            self._x = current_position['x']
            self._y = current_position['y']
            self._d = current_position['d']
        else:
            raise InvalidPosition

    def coordinates(self):
        return dict(x=self._x, y=self._y, d=self._d)

    def __str__(self):
        return "{},{},{}".format(self._x, self._y, self._d)

def parse_command(line):
    tokens = line.strip().split()

    command = tokens[0]
    if command not in {'MOVE', 'LEFT', 'RIGHT', 'REPORT', 'PLACE'}:
        raise InvalidCommand

    coordinates = None
    if command == 'PLACE':
        if len(tokens) < 2:
            raise InvalidCommand

        valid = ALLOWED_COMMANDS.search(tokens[1])
        if not valid:
            raise InvalidCommand

        coordinates = dict(
            x = int(valid['x']),
            y = int(valid['y']),
            d = valid['d'],
        )

    return command, coordinates

def current_position(method):
    def wrapper(self):
        if not self._position:
            return
        method(self)

    return wrapper


class Robot():

    _position = None

    def place(self, coordinates):
        try:
            self._position = Position(coordinates)
        except InvalidPosition:
            pass

    @current_position
    def move(self):
        current_position = self._position.coordinates()
        try:
            direction = current_position['d']
            if direction == 'NORTH':
                current_position['y'] += 1
            elif direction == 'EAST':
                current_position['x'] += 1
            elif direction == 'SOUTH':
                current_position['y'] -= 1
            elif direction == 'WEST':
                current_position['x'] -= 1

            self._position = Position(current_position)
        except InvalidPosition:
            pass

    @current_position
    def left(self):
        current_position = self._position.coordinates()
        try:
            direction = current_position['d']
            current_position['d'] = COMMANDS[direction]['left']
            self._position = Position(current_position)
        except InvalidPosition:
            pass

    @current_position
    def right(self):
        current_position = self._position.coordinates()
        try:
            direction = current_position['d']
            current_position['d'] = COMMANDS[direction]['right']
            self._position = Position(current_position)
        except InvalidPosition:
            pass

    @current_position
    def report(self):
        """Current position"""
        print(self._position)

def main():
  robot = Robot()
  for line in fileinput.input():
    try:
      (command, coordinates) = parse_command(line)
      if command == 'PLACE':
        robot.place(coordinates)
      else:
        getattr(robot, command.lower())()

    except InvalidCommand:
        pass


if __name__ == "__main__":
    main()
