import pygame
import sys
from random import randint


class Util:
    running = False

    # WIDTH = 640
    # HEIGHT = int(WIDTH / 12 * 9)

    WIDTH = 405
    HEIGHT = 300
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    tick = 0

    # colored
    '''yellow = (255, 255, 0)
    brown = (102, 51, 0)
    orange = (255, 128, 0)
    black = (0, 0, 0)
    green = (0, 255, 0)
    
    offset = 2'''

    # black and white
    yellow = (255, 255, 255)
    brown = (0, 0, 0)
    orange = (255, 255, 255)
    black = (255, 255, 255)
    green = (255, 255, 255)

    offset = 0


class Main:

    @staticmethod
    def run():
        Util.running = True
        pygame.init()
        pygame.display.set_caption("Snake")

        while Util.running:
            Util.clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    Input.input(1, event.key)
                if event.type == pygame.KEYUP:
                    Input.input(0, event.key)

            Engine.tick()

            Util.surface.fill(Util.brown)
            Engine.render()

            pygame.display.update()


class Objects:
    objectList = []
    tailList = []
    foodList = []

    def __init__(self, x, y, w, h, color, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xVel = 0
        self.yVel = 0
        self.color = color
        self.type = type

        # assigning object to appropriate lists
        Objects.objectList.append(self)
        if type == "tail" or type == "player":
            Objects.tailList.append(self)
        if type == "food":
            Objects.foodList.append(self)

    def setVel(self, dir, n):
        if dir.lower() == 'x':
            self.xVel = n
            self.yVel = 0
        if dir.lower() == 'y':
            self.yVel = n
            self.xVel = 0

    def delete(self):  # food only
        Objects.objectList.remove(self)
        Objects.foodList.remove(self)

    @staticmethod
    def grow():
        print("grew")
        Objects(Objects.tailList[-1].x, Objects.tailList[-1].y, player.w, player.h, player.color, "tail")

    @staticmethod
    def spawnFood():
        # to make the food as big as player
        w = Objects.objectList[0].w
        h = Objects.objectList[0].h
        Objects(randint(0, (Util.WIDTH / w) - 1) * w, randint(0, (Util.HEIGHT / h) - 1) * h, w, h, Util.green, "food")


# player dimensions have to divide with window dimensions
player = Objects(0, 0, 15, 15, Util.yellow, "player")  # has to be initialized first


class Input:
    player = Objects.objectList[0]

    @staticmethod
    def input(type, key):  # type is 0 or 1 - up or down - off or on
        if type == 1:
            if key == pygame.K_LEFT and player.xVel == 0:
                player.setVel('x', -1)
            elif key == pygame.K_RIGHT and player.xVel == 0:
                player.setVel('x', 1)

            elif key == pygame.K_UP and player.yVel == 0:
                player.setVel('y', -1)
            elif key == pygame.K_DOWN and player.yVel == 0:
                player.setVel('y', 1)

            '''if key == pygame.K_SPACE:
                Objects.spawnFood()'''


class Engine:
    player = Objects.objectList[0]

    @staticmethod
    def tick():
        # initial food spawning
        if Util.tick == 0:
            Objects.spawnFood()

        Util.tick += 1
        # calculating tail location
        for i in reversed(range(len(Objects.tailList))):
            if i == 0:
                pass
            else:
                Objects.tailList[i].x = Objects.tailList[i - 1].x
                Objects.tailList[i].y = Objects.tailList[i - 1].y

        # collision for food
        for item in Objects.foodList:
            if item.type != "player":
                if player.x == item.x and player.y == item.y:
                    Objects.delete(item)
                    Objects.grow()
                    Objects.spawnFood()

        # basic snake movement
        for item in Objects.tailList:
            item.x += item.xVel * player.w
            item.y += item.yVel * player.h

            # keeping snake in bounds
            if item.x >= Util.WIDTH:
                item.x = 0
            if item.x <= -player.w:
                item.x = Util.WIDTH - player.h

            if item.y >= Util.HEIGHT:
                item.y = 0
            if item.y <= -player.h:
                item.y = Util.HEIGHT - player.h

        # collision with self
        for item in Objects.tailList[1:]:  # 1: so it'd skip the first iteration (the head)
            if player.x == item.x and player.y == item.y:
                print("stopping")
                Util.running = False

    @staticmethod
    def pack(item, offset=0):
        return pygame.Rect(item.x + offset, item.y + offset, item.w - offset * 2, item.h - offset * 2)

    @staticmethod
    def render():
        for item in Objects.foodList:
            pygame.draw.rect(Util.surface, item.color, Engine.pack(item))

        # so snake would render ontop of food. Reversed so head would be rendered the last
        for item in reversed(Objects.tailList):
            pygame.draw.rect(Util.surface, item.color, Engine.pack(item, Util.offset))
            if item == Objects.tailList[0]:  # make the head a little different
                pygame.draw.rect(Util.surface, Util.black, Engine.pack(item, Util.offset * 2))


Main.run()
