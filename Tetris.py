import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
screen_width = 800
screen_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (screen_width - play_width) // 2  # Top left cordinate of the tetris playing area
top_left_y = screen_height - play_height       # Top left y - cordinate of the tetris playing area


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
     def __init__(self,x,y,shape):
         self.x = x
         self.y = y
         self.shape = shape
         self.color = shape_colors[shapes.index(self.shape)]
         self.rotation = 0


def create_grid(locked_positions={}):
     grid = [[(0,0,0) for i in range(10)]for j in range(20)]
     # locked positions will be a dictionary which will contain a position and a key value ie color

     for i in range(len(grid)):
         for j in range(len(grid[i])):
             if (j,i) in locked_positions:
                 c = locked_positions[(j,i)]  # c is the color corresponding to the j,i locked position
                 grid[i][j] = c
     return grid


# Most complex function
def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i,line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j,piece.y + i))

    # Now to adjust the positions of the pieces
    # in positions that we appended we are appending the positions of the 0's after .....
    # which will result in the final image bieng drawn to much to the left or down
    # so to adjust them we will subtract a temporary offset from the positions stored

    for i,pos in enumerate(positions):
        positions[i] = (pos[0]-2,pos[1]-4)
    return positions
def valid_space(shape, grid):
    accepted_pos = [[(j,i)for j in range(10) if grid[i][j]==(0,0,0)] for i in range(20)]

    # Now we will flatten the accepted_pos list
    accepted_pos = [j for sub in accepted_pos for j in sub]  # converts into a single list with no sublists
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1]>-1:
                return False
    return True



def check_lost(positions):
    for pos in positions:
        x,y = pos
        if y < 1:
            return True

    return False


def get_shape(): # this function will randomly select a falling shape
    return Piece(5,0,random.choice(shapes))


def draw_text_middle(surface,text,size,color):
    font = pygame.font.SysFont("comicsans",size,bold = True)
    label = font.render(text,1,color)

    surface.blit(label,(top_left_x+play_width/2-(label.get_width()/2),top_left_y+play_height/2-(label.get_height())/2))



def draw_grid(surface,grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface,(128,128,128),(sx,sy+i*block_size),(sx+play_width,sy+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx+j*block_size, sy), (sx + j*block_size, sy + play_height))


# This is the heart of the code ( Most Complex Part
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):   # for starting the loop backwards ( Means the bottomost grid row)
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1   # inc basically keeps track of how many rows got deleted
            ind = i    # to keep track of the index of the filled row
            for j in range(len(row)):
                try:
                    del locked[(j,i)] # This deletes the  filled row
                except:
                    continue
# Now after deleting tarow we need to shift the entire structure down and as one row got removed
# we need to add one on top to maintain the grid structure
    if inc > 0:
        for key in sorted(list(locked),key=lambda x : x[1])[::-1]:
            x,y = key
            if y<ind:   # that means this is above the deleted row and will move down
                newkeypos = (x,y+inc)
                locked[newkeypos] = locked.pop(key)  # We updated the element by moving it downwwards
                # as we know locked is dict of key value pair so basically the key is the position and we need the pos
                # to move downwards , color to remain same,so we need to update the pos of the element of the locked pso

# Main point to note is this where we will call this function
# Basically we will call this clear rows function whenever we are making the change_piece = True
# means whenever a piece hits the bottom most grid or whenever it comes in locked pos by colliding with other
# piece  we will check whether we need to clear any rows by calling this function

    return inc   # This is returned to monitor score as score will be proportional to the number of rows cleared


# This function will show you the next shape that will appear
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans",30)
    label = font.render('Next Shape',1,(255,255,255))

    sx = top_left_x + play_width + 50   # cordinate right of red box
    sy = top_left_y + play_height/2 - 100
    """top_left_x + playwidth is the cordinate just the corner of the red rectangle so to move it further to the right
       we need a constant"""
    # note that actually the shape argument that is passed here is actually the object of the piece
    # format will be the list containg the shape description of the correct piece ( i.e with positions)
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i,line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface,shape.color,(sx+j*block_size,sy+i*block_size,block_size,block_size),0)

    surface.blit(label,(sx+10,sy-30))

def update_score(game_score):

    score = max_score()
    with open('gamescore.txt','w') as f:
        if int(score) > game_score:   # Checking if the original score was greater or the new score based on that we update the score file
            f.write(str(score))
        else :
            f.write(str(game_score))

def max_score():
    with open('gamescore.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()  # .strip() is to remove all the "\n"

    return score

def draw_window(surface, grid,score = 0,last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    # Now the position where we want the label to be displayed in screen.blit
    x = top_left_x + play_width / 2 - (label.get_width() / 2)
    y = 30
    surface.blit(label, (x, y))

    # Current Score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render('Score  '+str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50  # cordinate right of red box
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label,(sx+20,sy+160))
    # Last Score
    # >>>>>>>>>>>>>>>>>>>>>>>> This PArt is for the implementation of the Highscore functionality>>>>>>>>>>>>>>>
    # label = font.render('High Score  ' + last_score, 1, (255, 255, 255))
    #
    # sx = top_left_x -200  # cordinate right of red box
    # sy = top_left_y + 200
    #
    # surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size,block_size,block_size),0)

            # 0 is for the fill argument that draw function fills the rectangle with the specified color
    # last argument after the rectangle position in pygame.draw.rect is width
    # if width == 0, (default) fill the rectangle
    # if width > 0, used for line thickness
    # if width < 0, nothing will be drawn

    # drawing the border of the tetris game
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface,grid)



def main(win):
    last_score = max_score()
    locked_pos = {}
    grid = create_grid(locked_pos)

    change_piece = False
    run = True
    curr_piece = get_shape()
    next_piece = get_shape()

    clock = pygame.time.Clock()
    fall_time = 0
    const_time = 0.27
    level_time = 0
    game_score =0
    while run:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5 :   # After every 5 seconds we will increase speed of the falling piece
            level_time = 0
            if level_time > 0.12:   # a threshold value after this decrease
                level_time-=0.005


        if fall_time/1000 > const_time:
            fall_time = 0
            curr_piece.y+=1
            if not(valid_space(curr_piece,grid)) and curr_piece.y > 0:
                curr_piece.y -=1
                change_piece = True
                # Think why its not a valid space even when you did not press any left or right button
                # either the current piece is hit onto other piece or its hit the bottom so we make change_piece = True



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = false
                sys.exit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                           curr_piece.x -=1
                           if not(valid_space(curr_piece,grid)):
                               # if the pos is not valid then nullify the above effect
                               curr_piece.x +=1
                if event.key == pygame.K_RIGHT:
                           curr_piece.x +=1
                           if not (valid_space(curr_piece, grid)):
                               # if the pos is not valid then nullify the above effect
                               curr_piece.x -= 1
                if event.key == pygame.K_DOWN:
                           curr_piece.y +=1
                           if not (valid_space(curr_piece, grid)):
                               # if the pos is not valid then nullify the above effect
                               curr_piece.y -= 1
                if event.key == pygame.K_UP:
                           curr_piece.rotation +=1
                           if not (valid_space(curr_piece, grid)):
                               # if the pos is not valid then nullify the above effect
                               curr_piece.rotation -= 1

        shape_pos = convert_shape_format(curr_piece)

        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y>-1:    # if y value of the piece is >-1 then only fill the grid with the shapes colors
                grid[y][x] = curr_piece.color  # Since the topmost part of the shape is the first pos in shape pos we only checked that parts y value because rest part of the shape is below it

        if change_piece:
           for pos in shape_pos:
               p = (pos[0],pos[1])
               locked_pos[p] = curr_piece.color    # note that locked pos is a dictionary holding a key value pair of
               # of positions and color and if the change_piece variable is true that means we need to change the current
               # shape cannot move further then we will add it in locked positions
           curr_piece = next_piece
           next_piece = get_shape()
           change_piece =   False
           game_score = clear_rows(grid,locked_pos) * 10



        draw_window(win,grid,game_score,last_score)
        draw_next_shape(next_piece,win)
        pygame.display.update()
        # Check if the game is over

        if check_lost(locked_pos):
            draw_text_middle(win,"You Lost!",80,(255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            # update_score(game_score)  for High score and Stuff
    # pygame.display.quit()

def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win,"Press Any Key to Play",60,(255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()


create_grid()
win = pygame.display.set_mode((screen_width,screen_height))   # Game window(win)
pygame.display.set_caption('Tetris')
main_menu(win)  # start game