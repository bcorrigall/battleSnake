# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import TheNode as node


theMap = [[node(x_cord=i, y_cord=j) for i in range(11)] for j in range(11)]

SNAKE_NAME = "My_Snake"


def updateNode(cords, value):
    theMap[cords["y"]]["x"].set_value(value)

def updateMap(board):
    for cords in board['food']:
        updateNode(cords, "food")

    for cords in board['hazards']:
        updateNode(cords, "hazard")

    for cords in board['snakes']["body"]:
        updateNode(cords, "snake")
    
    for snake in board['snakes']:
        if snake['name'] == SNAKE_NAME:
            updateNode(snake['head'], 'head')
            theMap[snake['head']['y']][snake['head']['x']].setDist(0)


def getNode(cords):
    return theMap[cords['y']][cords['y']]

def getDjikstras(head, objective):
    currentSet = [head]
    while True:
        nodes = []
        for current in currentSet:
            if (getNode(current).cord[0] == objective["x"]) and (getNode(current).cord[0] == objective['y']):
                return getBestNextMove(current), getNode(current).getDist()
            
            if getNode(current).visited == False:
                nodes.extend(getNeighbors(current))

            if(getNode(current).visited==False):
                theMap[current['y']][current['x']].setDist(getNode(current).getDist() + 1)
            
        
        currentSet = nodes
        if len(nodes) == 0:
            break

    return None, None

def getNeighbors(cords):

    pass

def evalNeighbors(curr, cordList):
    for cord in cordList:
        if(getNode(cord).visited==False):
            theMap[cord['y']][cord['x']].setDist(getNode(curr).getDist() + 1)

def getBestNextMove(current):
    #TODO Function that finds follows the shortest path, recursive?
    nodes = getNeighbors(current)

    for i in nodes:
        if getNode(i).getDist() ==0:
            return i

        if getNode(i).getDist() < getNode(current).getDist():
            return getBestNextMove(i)

def getDir(cord, head):
    if cord["x"] < head["x"]:
        return "left"
    
    if cord["x"] > head["x"]:
        return "right"
    
    if cord["y"] < head["y"]:
        return "down"
    
    if cord["y"] > head["y"]:
        return "up"



# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Snakes on a Plane",  # TODO: Your Battlesnake Username
        "color": "#FF0000",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins ]a game
def start(game_state: typing.Dict):
    # game_state]
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
        is_move_safe["left"] = False
    elif my_head["x"]+1 == board_width:
        is_move_safe["right"] = False

    if my_head["y"] == 0:
        is_move_safe["down"] = False
    elif my_head["y"]+1 == board_height:
        is_move_safe["up"] = False


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    
    if {"x" : my_head["x"]+1, "y" : my_head["y"]} in my_body:
        is_move_safe["right"] = False
    if {"x" : my_head["x"]-1, "y" : my_head["y"]} in my_body:
        is_move_safe["left"] = False
    if {"x" : my_head["x"], "y" : my_head["y"]+1} in my_body:
        is_move_safe["up"] = False
    if {"x" : my_head["x"], "y" : my_head["y"]-1} in my_body:
        is_move_safe["down"] = False



    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
