import pygame
import random
import copy
import sys
pygame.init()

# Size of each piece of the grid
gridSize = 20
# Dimensions of grid
dimensions = [20, 20]
screen = pygame.display.set_mode([gridSize * dimensions[0], gridSize * dimensions[1]])
clock = pygame.time.Clock()


class Segment:
    def __init__(self, pos, direction, color):
        self.pos = pos
        self.direction = direction
        self.color = color


class Snake:
    body = []
    for i in range(3):
        body.append(Segment([(int(dimensions[0]/2) - i), (int(dimensions[1]/2))], [1, 0], [0, 0, 0]))
    tail = copy.deepcopy(body[len(body) - 1])

    def move(self):
        self.tail = copy.deepcopy(self.body[len(self.body) - 1])
        for i in self.body:
            i.pos[0] += i.direction[0]
            i.pos[1] += i.direction[1]
            # want to go through every segment except the leading one in descending order
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].direction = self.body[i - 1].direction

    def display(self):
        for i in self.body:
            pygame.draw.rect(screen, (255, 255, 255), (i.pos[0] * gridSize, i.pos[1] * gridSize, gridSize, gridSize))

    def grow(self):
        self.body.append(copy.deepcopy(self.tail))


class Food:
    def __init__ (self, pos):
        self.pos = pos
        self.color = (255, 0, 0)

    def move(self):
        # Check board to find unoccupied space
        # move food to that space
        valid = False
        while not valid:
            self.pos = [random.randint(0, dimensions[0] - 1), random.randint(0, dimensions[1] - 1)]
            for i in snake.body:
                if i.pos == self.pos:
                    #print(" Occupied space:", self.pos)
                    valid = False
                    break
                else:
                    #print(" Unoccupied space: food -", self.pos, "snake -", i.pos)
                    valid = True

    def display(self):
        #pygame.draw.rect(screen, color, (left, top, width, height))
        pygame.draw.rect(screen, (255, 0, 0), (self.pos[0] * gridSize, self.pos[1] * gridSize, gridSize, gridSize), 0)


# End of Classes/functions

# Create the snake and food and place them on the canvas
snake = Snake()
snake.body[0].color = (0, 255, 0)
# Food spawns at a random location inside the screen
food = Food([random.randint(0, dimensions[0] - 1), random.randint(0, dimensions[1] - 1)])


while True:
    # If the red X in the window is clicked close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # Update the screen as well as make it black
    pygame.display.update()
    screen.fill((0, 0, 0))

    # Check for keypress to see if the user wants to change direction
    key = pygame.key.get_pressed()
    # UP
    if key[pygame.K_UP] or key[pygame.K_w] and snake.body[0].direction != [0,1]:
        snake.body[0].direction = [0, -1]
        print("up", snake.body[0].direction)
    # RIGHT
    elif key[pygame.K_RIGHT] or key[pygame.K_d] and snake.body[0].direction != [-1,0]:
        snake.body[0].direction = [1, 0]
        print("right", snake.body[0].direction)
    # DOWN
    elif key[pygame.K_DOWN] or key[pygame.K_s] and snake.body[0].direction != [0,-1]:
        snake.body[0].direction = [0, 1]
        print("down", snake.body[0].direction)
    # LEFT
    elif key[pygame.K_LEFT] or key[pygame.K_a] and snake.body[0].direction != [1,0]:
        snake.body[0].direction = [-1, 0]
        print("left", snake.body[0].direction)
    else:
        pass

    # Speed of the game
    clock.tick(7)

    snake.move()
    # If the leading segment hits either a boundary or another segment of the snake it dies

    #for i in snake.body:
    #    print(i.pos, end=" ")
    #print()

    if (snake.body[0].pos == food.pos):
        print("Eatin at:", food.pos)
        print("Snake length:", len(snake.body))
        snake.grow()
        food.move()

    # Display the food and then the snake so the snake overlaps the food
    food.display()
    snake.display()
