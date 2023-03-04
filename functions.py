DIRECTIONS = ['up', 'down', 'left', 'right']

DELTAS = {
    'up': {'x':  0, 'y': -1, },
    'down': {'x':  0, 'y': +1, },
    'left': {'x': -1, 'y':  0, },
    'right': {'x': +1, 'y':  0, },
}

NO_DISTANCE = -1
NO_MOVE = '?'

DEBUG = False


class Game(object):
    def __init__(self, data, exclude_heads_of_other_snakes):
        board_data = data['board']
        self.height = board_data['height']
        self.width = board_data['width']
        self.food = board_data['food']
        self.board = [[0 for _ in range(self.width)]
                      for _ in range(self.height)]
        you = data['you']
        self.id = you['id']
        self.name = you['name']
        body = you['body']
        self.health = you['health']
        self.head = body[0]

        snakes = board_data['snakes']
        for snake in snakes:
            for part in snake['body'][:-1]:
                self.board[part['y']][part['x']] = 1
            if exclude_heads_of_other_snakes:
                if snake['id'] != self.id and len(snake['body']) >= len(body):
                    head = snake['body'][0]
                    for (_, nx, ny) in self.adjacent(head['x'], head['y']):
                        self.board[ny][nx] = 1

    def adjacent(self, x, y):
        res = []
        for direction in DIRECTIONS:
            delta = DELTAS[direction]
            nx = x + delta['x']
            ny = y + delta['y']
            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height and self.board[ny][nx] == 0:
                res.append((direction, nx, ny))
        return res


def distances(self, x, y):
    res = [[NO_DISTANCE for _ in range(self.width)]
           for _ in range(self.height)]
    move = [[NO_MOVE for _ in range(self.width)]
            for _ in range(self.height)]
    move_debug = [[NO_MOVE for _ in range(
        self.width)] for _ in range(self.height)]
    # Flood fill.
    res[y][x] = 0
    deque = collections.deque()
    for (m, nx, ny) in self.adjacent(x, y):
        deque.append((nx, ny, 1, m))
    while deque:
        (x, y, d, m) = deque.popleft()
        if res[y][x] != NO_DISTANCE:
            continue
        res[y][x] = d
        move[y][x] = m
        move_debug[y][x] = m[0]
        for (_, nx, ny) in self.adjacent(x, y):
            if res[ny][nx] == NO_DISTANCE:
                deque.append((nx, ny, d + 1, m))
    return res, move, move_debug

    def move_to_pos(self, x, y, moves):
        res = moves[y][x]
        return res

    def move_to_max(self, distances, moves):
        maxdist = -1
        res = NO_MOVE
        for x in range(self.width):
            for y in range(self.height):
                if distances[y][x] > maxdist:
                    maxdist = distances[y][x]
        return res


def move_to_food(self, distances, moves, tail_distances):
    res = NO_MOVE
    mindist = sys.maxint
    for food in self.food:
        x = food['x']
        y = food['y']
        dist = distances[y][x]
        if dist != NO_DISTANCE and (dist < mindist) and (
                (tail_distances[y][x] != NO_DISTANCE and tail_distances[y][x] >= 2) or self.health <= 25):
            mindist = dist
            res = moves[y][x]
    return res


def get_min_health(name):
    res = 100
    if "health_50" in name:
        res = 50
    return res


def run(data, exclude_heads_of_other_snakes):

    game = Game(data, exclude_heads_of_other_snakes)
    distances, moves, moves_debug = game.distances(
        game.head['x'], game.head['y'])
    tail_distances, _, _ = game.distances(game.tail['x'], game.tail['y'])
    tails = [(_, game.tail['x'], game.tail['y'])] + \
        game.adjacent(game.tail['x'], game.tail['y'])
    for (_, x, y) in tails:
        direction = game.move_to_pos(x, y, moves)
        if direction != NO_MOVE:
            break
    if direction == NO_MOVE:
        direction = game.move_to_max(distances, moves)
    if game.health <= get_min_health(game.name):
        food_direction = game.move_to_food(distances, moves, tail_distances)
        if food_direction != NO_MOVE:
    return direction