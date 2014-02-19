import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Girl"
    def __init__(self):
        GameElement.__init__(self)
        self.isAlive = True
        self.inventory = []

    def die(self):
        self.isAlive = False
        
        
        return time.sleep(20)
        # enter = raw_input('<<  ')
        # if enter:
        #     sys.exit()
   
    def next_pos(self, direction):
        # if character is dead, direction = null
        if self.isAlive == False:
            # Key.keyboard_handler = None
            self.die()
        else:
            if direction == "up":
                return (self.x, self.y-1)
            elif direction == "down":
                return (self.x, self.y+1)
            elif direction == "left":
                return (self.x-1, self.y)
            elif direction == "right":
                return (self.x+1, self.y)
         



        # if Character touches [range of possible chars that can kill it]:
        # screen fills up with something
        # message of some kind
        # disable movement
         


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self,PLAYER):
        PLAYER.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(PLAYER.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self,PLAYER):
        PLAYER.inventory.append(self)
        GAME_BOARD.draw_msg("You have the key! You can open doors!")

class Door(GameElement):

    IMAGE = "DoorClosed"
    SOLID = True
    OPEN = False        

    def interact(self, PLAYER):
        print PLAYER.inventory
        print PLAYER.inventory[0]
        for i in range(len(PLAYER.inventory)):
            if type(PLAYER.inventory[i]) == Key:
                Door.OPEN = True
                Door.IMAGE = "DoorOpen"
            # if PLAYER.x > Door.x:
            #     Door.IMAGE = "DoorOpen"
            #     PLAYER.x += 2

class Cat(GameElement):
    IMAGE = "Cat"
    def interact(self,PLAYER):
        GAME_BOARD.draw_msg('game over')
        PLAYER.isAlive = False


        # else:
        #     GAME_BOARD.draw_msg('You need the key to open the door.')
    # if have key, can open door:

    # else:
        # door remains closed, have message stating this

   



####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    GAME_BOARD.draw_msg("This game is awesome.")
    
    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        print 'rock is instantiated ', rock
        GAME_BOARD.register(rock)
        print 'game board is instantiated',GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    # for rock in rocks:
    #     print rock
    # door = Door()
    # GAME_BOARD.register(door)
    # GAME_BOARD.set_el(5,3,door)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    # key = Key()
    # GAME_BOARD.register(key)
    # GAME_BOARD.set_el(4, 3, key)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)

    print PLAYER

    cat = Cat()
    GAME_BOARD.register(cat)
    GAME_BOARD.set_el(6, 5, cat)





def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
        if 0 > next_y or next_y >= 7 or 0 > next_x or next_x >= 7:
            next_x = PLAYER.x
            next_y = PLAYER.y
            GAME_BOARD.draw_msg("You fool! You can't go off the ends of the earth")

        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
        if existing_el:
            existing_el.interact(PLAYER)
            if type(existing_el) == Door:
                print "it's a door"
                # is door open?
                if Door.OPEN:
                    print 'this is true'
                    if PLAYER.x < next_x:
                        PLAYER.x += 2
                        #GAME_BOARD.del_el(PLAYER.x-2, PLAYER.y)
                        #To keep a clone, don't delete the player
                        Door.OPEN = False
                    elif PLAYER.x > next_x:
                         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                         PLAYER.x -= 1
                         Door.OPEN = False
                    # if PLAYER.y < next_y:
                    #     PLAYER.y += 2
                    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y-2)
                    #     Door.OPEN = False
                    # if PLAYER.y > next_y:                
                    #     PLAYER.y -= 2
                    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y+2)
                    #     Door.OPEN = False

    # if KEYBOARD[key.UP]:
    #     GAME_BOARD.draw_msg("You pressed up")
    #     next_y = PLAYER.y - 1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    # if KEYBOARD[key.DOWN]:
    #     GAME_BOARD.draw_msg("You pressed down.")
    #     next_y = PLAYER.y + 1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    # if KEYBOARD[key.RIGHT]:
    #     GAME_BOARD.draw_msg("You pressed right.")
    #     next_x = PLAYER.x + 1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    # if KEYBOARD[key.LEFT]:
    #     GAME_BOARD.draw_msg("You pressed left.")
    #     next_x = PLAYER.x - 1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    # elif KEYBOARD[key.SPACE]:
    #     GAME_BOARD.erase_msg()



    # rock1 = Rock()
    # GAME_BOARD.register(rock1)
    # GAME_BOARD.set_el(2,1,rock1)

    # rock2 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(1,2, rock2)

    # rock3 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(3,2, rock2)

    # rock4 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(2,3, rock2)

    # print "The first rock is at", (rock1.x, rock1.y)
    # print "The second rock is at", (rock2.x, rock2.y)
    # print "The third rock is at", (rock3.x, rock3.y)
    # print "The fourth rock is at", (rock4.x, rock4.y)

    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE



