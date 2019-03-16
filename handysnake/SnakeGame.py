import random
import pygame
import sys
from pygame.locals import *

#Game settings and iniatialization
global FPS
FPS = 5
screenWidth = 800
screenHeight = 600
cellSize = 20

assert screenHeight % cellSize == 0, "Window Height must be a multiple of Cell Size"
assert screenWidth % cellSize == 0, "Window Width must be a multiple of Cell Size"

cellWidth = int(screenWidth / cellSize)
cellHeight = int(screenHeight / cellSize)

#Colour Codes in RGB format
WHITE    = (255, 255, 255)
BLACK    = (0,     0,   0)
RED      = (255,   0,   0)
DARKGREEN= (0,   155,   0)
DARKGRAY = (40,   40,  40)
YELLOW   = (255, 255,   0)
LIGHTGRAY = (190, 190, 190)

SNAKE_BG = (34, 153, 24)
SNAKE_BODY = BLACK
SNAKE_HEAD = WHITE

BGCOLOR = DARKGREEN

#Control/Direction Keys
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#Index of the snake's head
HEAD = 0 


def main():
        global clock, displayScreen, font

        pygame.init()
        clock = pygame.time.Clock()
        displayScreen = pygame.display.set_mode((screenWidth, screenHeight))
        font = pygame.font.SysFont('Fixedsys Regular', 35)
        pygame.display.set_caption('Handy Snake')

        

        showStartdisplayScreen()
        while True:
                runGame()
                level = 1
                drawLevel(level)
                selectLevel(level)
                showGameOverdisplayScreen()

                
                
def runGame():
        #Set a random starting point
        startx = random.randint(5, cellWidth - 6)
        starty = random.randint(5, cellHeight - 6)
        global snakecoordinates
        snakecoordinates = [{'x' : startx, 'y' : starty}, {'x': startx - 1, 'y':starty}, {'x':startx - 2, 'y':starty}]
        direction = RIGHT

        apple = getRandomLocation()

        while True:
                for event in pygame.event.get():
                        if event.type == QUIT:
                                terminate()
                        elif event.type == KEYDOWN:
                                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                                        direction = LEFT
                                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                                        direction = RIGHT
                                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                                        direction = UP
                                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                                        direction = DOWN
                                elif event.key == K_ESCAPE:
                                        terminate()

#Code to detect collisions
        
        #Detect Collision with edges
                if snakecoordinates[HEAD]['x'] == -1 or snakecoordinates[HEAD]['x'] == cellWidth or snakecoordinates[HEAD]['y'] == -1 or snakecoordinates[HEAD]['y'] == cellHeight:
                        return
        
        #Detect Collision with snake's own body
                for snakeBody in snakecoordinates[1:]:
                        if snakeBody['x'] == snakecoordinates[HEAD]['x'] and snakeBody['y'] == snakecoordinates[HEAD]['y']:
                                return
       
        #Check if Apple is eaten
                if snakecoordinates[HEAD]['x'] == apple['x'] and snakecoordinates[HEAD]['y'] == apple['y']:
                        apple = getRandomLocation()
                else:
                        del snakecoordinates[-1]


        #Increase level of the game
                currentScore = getTotalScore()
                if(currentScore >= 20 and currentScore < 50):
                    level = 2
                    drawLevel(level)
                    selectLevel(level)
                elif(currentScore >= 50 and currentScore < 90):
                    level = 3
                    drawLevel(level)
                    selectLevel(level)
                elif(currentScore >= 90 and currentScore < 150):
                    level = 4
                    drawLevel(level)
                    selectLevel(level)
                elif(currentScore >=150 and currentScore < 200):
                    level = 5
                    drawLevel(level)
                    selectLevel(level)
                elif(currentScore >= 200 and currentScore < 300):
                    level = 6
                    drawLevel(level)
                    selectLevel(level)
                elif(currentScore >= 300 and currentScore < 400):
                    level = 7
                    drawLevel(level)
                    selectLevel(level)
                elif(currentScore >=400 and currentScore < 550):
                    level = 8
                    drawLevel(level)
                    selectLevel(level)

#Give directions to the Snake
                if direction == UP:
                        newHead = {'x': snakecoordinates[HEAD]['x'], 'y': snakecoordinates[HEAD]['y'] - 1}
                elif direction == DOWN:
                        newHead = {'x': snakecoordinates[HEAD]['x'], 'y': snakecoordinates[HEAD]['y'] + 1}
                elif direction == RIGHT:
                        newHead = {'x': snakecoordinates[HEAD]['x'] + 1, 'y': snakecoordinates[HEAD]['y']}
                elif direction == LEFT:
                        newHead = {'x': snakecoordinates[HEAD]['x'] - 1, 'y': snakecoordinates[HEAD]['y']}
                snakecoordinates.insert(0, newHead)

#Display the Game Screen
                displayScreen.fill(SNAKE_BG)
                drawBackGroundGrid()
                drawSnake(snakecoordinates)
                placeApple(apple)
                drawScore((len(snakecoordinates) - 3) * 10)
                pygame.display.update()
                clock.tick(FPS)


#Display press any key to play message
def drawPressAnyKeyMsg():
        pressKeyText = font.render('Press Any Key To Play', True, YELLOW)
        pressKeyRect = pressKeyText.get_rect()
        pressKeyRect.center = (screenWidth / 2, screenHeight - 100)
        displayScreen.blit(pressKeyText, pressKeyRect)

#checks if any key is pressed
def checkForKeyPress():
        if len(pygame.event.get(QUIT)) > 0:
                terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
                return None
        if keyUpEvents[0].key == K_ESCAPE:
                terminate()
        return keyUpEvents[0].key

#function to display the main home screen of the game
def showStartdisplayScreen():
        title_font = pygame.font.SysFont('Fixedsys Regular', 100)
        title_text = title_font.render('Handy Snake', True, BLACK)
        while True:
                img = pygame.image.load('snake.jpg')
                displayScreen.fill(BGCOLOR)
                title_text_rect = title_text.get_rect()
                title_text_rect.center = (screenWidth / 2, screenHeight / 6)
                displayScreen.blit(title_text, title_text_rect)
                img_rect = img.get_rect()
                img_rect.center = (screenWidth / 2, screenHeight / 2)
                displayScreen.blit(img, img_rect)

                drawPressAnyKeyMsg()
                if checkForKeyPress():
                        pygame.event.get()
                        return
                pygame.display.update()
                clock.tick(FPS)

#function to display game over screen and the total score
def showGameOverdisplayScreen():
        gameOverfont = pygame.font.SysFont('Fixedsys Regular', 80)
        gameOverText = gameOverfont.render('Game Over', True, WHITE)
        gameOverRect = gameOverText.get_rect()
        
        totalscorefont = pygame.font.SysFont('Fixedsys Regular', 30)
        totalscoreText = totalscorefont.render('Total Score: %s' % (getTotalScore()), True, WHITE)
        totalscoreRect = totalscoreText.get_rect()
        
        totalscoreRect.midtop = (screenWidth/2, 150)
        gameOverRect.midtop = (screenWidth/2, 30)
        
        displayScreen.fill(BGCOLOR)
        
        displayScreen.blit(gameOverText, gameOverRect)
        displayScreen.blit(totalscoreText, totalscoreRect)
        
        drawPressAnyKeyMsg()
        
        pygame.display.update()
        pygame.time.wait(1000)
        
        checkForKeyPress()

        while True:
                if checkForKeyPress():
                        pygame.event.get()
                        return

#function to create/display the snake
def drawSnake(snakecoordinates):
        x = snakecoordinates[HEAD]['x'] * cellSize
        y = snakecoordinates[HEAD]['y'] * cellSize
        snakeHeadRect = pygame.Rect(x, y, cellSize, cellSize)
        pygame.draw.rect(displayScreen, SNAKE_HEAD, snakeHeadRect)

        for coordinates in snakecoordinates[1:]:
                x = coordinates['x'] * cellSize
                y = coordinates['y'] * cellSize
                snakeSegmentRect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(displayScreen, SNAKE_BODY, snakeSegmentRect)

#function to place the apple at a particular position
def placeApple(coordinates):
        x = coordinates['x'] * cellSize
        y = coordinates['y'] * cellSize
        pygame.draw.circle(displayScreen, RED, (int(x + cellSize/2), int(y + cellSize/2)), int(cellSize/2), 0)

#fuction to create a grid system for the game window
def drawBackGroundGrid():
        for x in range(0, screenWidth, cellSize):
                pygame.draw.line(displayScreen, LIGHTGRAY, (x, 0), (x, screenHeight))
        for y in range(0, screenHeight, cellSize):
                pygame.draw.line(displayScreen, LIGHTGRAY, (0, y), (screenWidth, y))

#function to display real-time score on the game window
def drawScore(score):
        scoreText = font.render('Score: %s' % (score), True, WHITE)
        scoreRect = scoreText.get_rect()
        scoreRect.center = (screenWidth - 100, 30)
        displayScreen.blit(scoreText, scoreRect)
                
#function to generate random location for apples
def getRandomLocation():
        return {'x': random.randint(0, cellWidth - 1), 'y': random.randint(0, cellHeight - 1)}

#gives total score of a player at any point of time during the game
def getTotalScore():
        return ((len(snakecoordinates) - 3) * 10)                

#function to change level which in-turn increases the snake's speed 
def selectLevel(level):
    global FPS
    if level == 1:
        FPS = 5
    elif level == 2:
        FPS = 7
    elif level == 3:
        FPS = 9
    elif level == 4:
        FPS = 11
    elif level == 5:
        FPS = 13
    elif level == 6:
        FPS = 15
    elif level == 7:
        FPS = 17
    elif level == 8:
        FPS = 19

#function to change the title of the window every time the level is increased
def drawLevel(level):
        pygame.display.set_caption('Handy Snake Level %s' %(level))
        
#exit game 
def terminate():
        pygame.quit()
        sys.exit()        

if __name__ == '__main__':
        main()
