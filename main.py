
from astar import *
import bottle
import copy
import math
import os

SNAKE_BUFFER = 3
ID = 'de508402-17c8-4ac7-ab0b-f96cb53fbee8'
SNAKE = 1
WALL = 2
FOOD = 3
GOLD = 4
SAFETY = 5


def goals(data):
    result = data['food']
    if data['mode'] == 'advanced':
        result.extend(data['gold'])
    return result


def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'east'
    elif dx == -1:
        return 'west'
    elif dy == -1:
        return 'north'
    elif dy == 1:
        return 'south'


def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy


def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item


def init(data):
    grid = [[0 for col in xrange(data['height'])]
            for row in xrange(data['width'])]
    for SNAKE in data['snakes']:
        if SNAKE['id'] == ID:
            mysnake = SNAKE
        for coord in SNAKE['coords']:
            grid[coord[0]][coord[1]] = SNAKE

    if data['mode'] == 'advanced':
        for wall in data['walls']:
            grid[wall[0]][wall[1]] = WALL
        for g in data['gold']:
            grid[g[0]][g[1]] = GOLD

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return mysnake, grid


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/Traitor.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }
# DATA OBJECT
# {
#     "game": "hairy-cheese",
#     "mode": "advanced",
#     "turn": 4,
#     "height": 20,
#     "width": 30,
#     "snakes": [
#         <Snake Object>, <Snake Object>, ...
#     ],
#     "food": [
#         [1, 2], [9, 3], ...
#     ],
#     "walls": [    // Advanced Only
#         [2, 2]
#     ],
#     "gold": [     // Advanced Only
#         [5, 5]
#     ]
# }

# SNAKE
# {
#     "id": "1234-567890-123456-7890",
#     "name": "Well Documented Snake",
#     "status": "alive",
#     "message": "Moved north",
#     "taunt": "Let's rock!",
#     "age": 56,
#     "health": 83,
#     "coords": [ [1, 1], [1, 2], [2, 2] ],
#     "kills": 4,
#     "food": 12,
#     "gold": 2
# }


@bottle.post('/move')
def move():
    data = bottle.request.json
    SNAKE, grid = init(data)

    # foreach snake
    for enemy in data['snakes']:
        if (enemy['id'] == ID):
            continue
        if distance(SNAKE['coords'][0], enemy['coords'][0]) > SNAKE_BUFFER:
            continue
        if (len(enemy['coords']) > len(SNAKE['coords'])-1):
            # dodge
            if enemy['coords'][0][1] < data['height']-1:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1]+1] = SAFETY
            if enemy['coords'][0][1] > 0:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1]-1] = SAFETY

            if enemy['coords'][0][0] < data['width']-1:
                grid[enemy['coords'][0][0]+1][enemy['coords'][0][1]] = SAFETY
            if enemy['coords'][0][0] > 0:
                grid[enemy['coords'][0][0]-1][enemy['coords'][0][1]] = SAFETY

    SNAKE_head = SNAKE['coords'][0]
    SNAKE_coords = SNAKE['coords']
    path = None
    middle = [data['width'] / 2, data['height'] / 2]
    foods = sorted(data['food'], key=lambda p: distance(p, middle))
    if data['mode'] == 'advanced':
        foods = data['gold'] + foods
    for food in foods:
        # print food
        tentative_path = a_star(SNAKE_head, food, grid, SNAKE_coords)
        if not tentative_path:
            # print "no path to food"
            continue

        path_length = len(tentative_path)
        SNAKE_length = len(SNAKE_coords) + 1

        dead = False
        for enemy in data['snakes']:
            if enemy['id'] == ID:
                continue
            if path_length > distance(enemy['coords'][0], food):
                dead = True
        if dead:
            continue

        # Update SNAKE
        if path_length < SNAKE_length:
            remainder = SNAKE_length - path_length
            new_SNAKE_coords = list(
                reversed(tentative_path)) + SNAKE_coords[:remainder]
        else:
            new_SNAKE_coords = list(reversed(tentative_path))[:SNAKE_length]

        if grid[new_SNAKE_coords[0][0]][new_SNAKE_coords[0][1]] == FOOD:
            # we ate food so we grow
            new_SNAKE_coords.append(new_SNAKE_coords[-1])

        # Create a new grid with the updates SNAKE positions
        new_grid = copy.deepcopy(grid)

        for coord in SNAKE_coords:
            new_grid[coord[0]][coord[1]] = 0
        for coord in new_SNAKE_coords:
            new_grid[coord[0]][coord[1]] = SNAKE

        # printg(grid, 'orig')
        # printg(new_grid, 'new')

        # print SNAKE['coords'][-1]
        foodtotail = a_star(
            food, new_SNAKE_coords[-1], new_grid, new_SNAKE_coords)
        if foodtotail:
            path = tentative_path
            break
        # print "no path to tail from food"

    if not path:
        path = a_star(SNAKE_head, SNAKE['coords'][-1], grid, SNAKE_coords)

    despair = not (path and len(path) > 1)

    if despair:
        for neighbour in neighbours(SNAKE_head, grid, 0, SNAKE_coords, [1, 2, 5]):
            path = a_star(SNAKE_head, neighbour, grid, SNAKE_coords)
            # print 'i\'m scared'
            break

    despair = not (path and len(path) > 1)

    if despair:
        for neighbour in neighbours(SNAKE_head, grid, 0, SNAKE_coords, [1, 2]):
            path = a_star(SNAKE_head, neighbour, grid, SNAKE_coords)
            # print 'lik so scared'
            break

    if path:
        assert path[0] == tuple(SNAKE_head)
        assert len(path) > 1

    return {
        'move': direction(path[0], path[1]),
        'taunt': 'TRAITOR!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'Boa Down!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv(
        'IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
