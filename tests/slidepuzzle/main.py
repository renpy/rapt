# Slide Puzzle
# http://inventwithpython.com/blog
# By Al Sweigart al@inventwithpython.com

"""
Welcome to the Code Comments for Simulate. Code Comments is a series of simple games with detailed comments in the source code, so you can see how the game works.

The text in between the triple-double-quotes are comments. The Python interpreter ignores any text in between them, so we can add any comments about the source code without affecting the program. In general for Code Comments, the comments will describe the lines of code above the comment. It helps to view this file either on the Code Comments site or with a text editor that does "syntax highlighting", so that the comments appear in a separate color and are easier to distinguish from the code.

This Code Comments assumes you know some basic Python programming. If you are a beginner and would like to learn computer programming, there is a free book online called "Invent Your Own Computer Games with Python" at http://inventwithpython.com

The Code Comments programs make references to sections of this book throughout the program. This Code Comments can also teach you how to use the Pygame library to make your own games with graphics, animation, and sound. You can download Pygame from http://pygame.org and view its documentation at http://pygame.org/docs/

HOW TO PLAY SLIDE PUZZLE
There are 15 tiles in a 4x4 grid. At the start of the game, the tiles are randomly switched around the board to generate a new puzzle. When the puzzle is ready, start sliding around the tilees to reorder the tiles.
"""

import pygame, sys, random, time
from pygame.locals import *
"""Here we import modules that our game needs. random has random number functions, time has the sleep() function, sys has the exit() function, and pygame contains all the pygame-related functions.

pygame.locals contains constants like MOUSEMOTION and MOUSEBUTTONUP and QUIT for the events. It's easier to type MOUSEBUTTONUP instead of pygame.locals.MOUSEBUTTONUP, so we use the "from pygame.locals import *" format to import these to the local namespace.
"""

try:
    import android
except ImportError:
    android = None
    
# Create the constants (change these to different values to modify the game.)
COLS = 4
ROWS = 4
TILESIZE = 100
WINDOWWIDTH = 480
WINDOWHEIGHT = 800
FPS = 30
"""These constant variables (the uppercase names means we shouldn't change the values stored in them) set some standard values for our game. You can play around with different values for them (though some values might cause bugs in the game.) By using constants instead of the values directly, it is easier to make changes since we only have to change them in one place.

For example, if we used 80 instead of TILESIZE, then if we wanted to change our code later we'd have to change every place in the code we find 80. This is trickier than just changing the one line where MAXLIFE is originally set.

More information about constants is at http://inventwithpython.com/chapter9.html#ConstantVariables
"""

# Create the color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
BLUE = (0, 153, 153)
GREEN = (0, 204, 0)

BGCOLOR = BLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
FONTSIZE = 40

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
"""We also set up some constant values for different colors. Pygame uses tuples of three integers to represent color. The integers represent the amount of red, green, and blue in the color (this is commonly called a RGB). 0 means there is none of the primary color in the color, and 255 means there is the maximum amount. So (255, 0, 0) is red, since it has the maximum amount of red but no green or blue. But (255, 0, 255) adds the max amount of blue with the red, creating purple.

More information about colors is at http://inventwithpython.com/chapter17.html#ColorsinPygame
"""

# Other constants and global variables.
RESET_SURF = None
RESET_RECT = None
NEW_SURF = None
NEW_RECT = None
SOLVE_SURF = None
SOLVE_RECT = None

XMARGIN = int((WINDOWWIDTH - (TILESIZE * COLS + (COLS - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * ROWS + (ROWS - 1))) / 2)
"""We need to calculate the amount of space that is on the side of the tiles. We do this by taking the size of the window, subtract the width of the tiles (times the number of columns of tiles). But we also want to take into account the pixels in between the tiles. These gaps are one pixel in size each, and there are (COLS - 1) of them. So we subtract this value from the window width too. Then, since there are two margins on either side of the tiles, we divide the numbr we have by 2.

We do the same for the Y margin."""

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

"""We need values for each of the directions up, down, left, and right in our program. These can be any four distinct values, as long as they are used consistently it won't matter to our program. We could use the strings 'up', 'down', etc. Instead, we'll use constant variables.

The difference is if we make a typo using the strings, Python won't crash but it will still cause a bug. For instance, if we had this bit of code:
    if direction == 'dwon':
...then the program will still run, but it would contain a bug because if the direction variable was set to 'down', this condition would still evaluate to False (which is not how we'd want the code to behave).

But if we use constant values instead and make a similar typo:
    if direction == DWON:
...then Python crashes when it comes across this line because there is no such variable as DWON, just DOWN. Why is crashing a good thing? Well, it's not, but in this case it would immediately alert us that there is a problem, and we could fix it. If we had used a string instead, it might take a while to track down where the bug is caused. Using constants in this way helps us ensure that our program works correctly.
"""

def main():
    global MAINCLOCK, MAINSURF, FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    """The main() function is where our program begins. (See the last two lines of code to see why.) Because we define MAINCLOCK and MAINSURF inside this function, these are local variables to the main() function and the names MAINCLOCK and MAINSURF won't exist outside of this function. By using a global statement, we can tell Python that we want these variables to be global variables.

    More information about global and local variables is at http://inventwithpython.com/chapter6.html#VariableScope
    """

    pygame.init()
    if android:
        android.init()
    MAINCLOCK = pygame.time.Clock()
    MAINSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')

    """pygame.init() needs to be called before any of the other Pygame functions.

    pygame.time.Clock() returns a pygame.Clock object. We will use this object's tick() method to ensure that the program runs at no faster than 30 frames per second (or whatever integer value we have in the FPS constant.)

    pygame.display.set_mode() creates the window on the screen and returns a pygame.Surface object. Any drawing done on this Surface object with the pygame.draw.* functions will be displayed on the screen when we call pygame.display.update().

    More information about pygame.display.set_mode() is at http://inventwithpython.com/chapter17.html#ThepygamedisplaysetmodeandpygamedisplaysetcaptionFunctions"""

    FONT = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    """This line loads a font to use for drawing text. Since our game only uses one font (and at one size, 16 points) we only have to make one call to the pygame.font.Font() constructor function. We will store this font in the global variable FONT."""

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 240, WINDOWHEIGHT - 180)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 240, WINDOWHEIGHT - 120)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 240, WINDOWHEIGHT - 60)
    """Our program needs three buttons for reset the game, starting a new game, and solving the current puzzle. The data for these buttons will be made by our makeText() function, which is described later. makeText() will return two objects, a surface object that contains the text and a rectangle object that contains the position and size data of the button.

    Here we are just creating the objects for the button. We will display them on the screen in the drawBoard() function."""

    mainBoard, solutionSeq = generateNewPuzzle(80)
    """generateNewPuzzle() will create a new puzzle by creating a new data structure for our board and then randomly sliding the puzzle around 100 times. It will remember the sequence of slides it made and return that along with the board data structure.

    The structure of the board data structure is described in detail in generateNewPuzzle(), but basically it's a list of list of integers, where the integers correspond to the number on the tile and the 0 integer stands for the blank space.

    Since we keep a record of the slides that were made, we could always do the reverse of those slides to get the board back to its original state. This is how we "solve" the board when the player pushes on the Solve button."""

    solvedBoard = getStartingBoard() # a solved board is the same as the board in a start state.
    """We're going to make a board that is in the ordered, starting state around so we can compare it to the board that is displayed on the screen (that is, mainBoard). If these two boards are equal, we know that the player has solved the board."""
    seq = []
    """We are also going to keep a record of the player's slides, so we can revert back to the start of the puzzle if the player wants. (We also need to know this if we want to automatically solve the puzzle."""

    while True:
        # The main game loop.
        sliding = None
        msg = ''
        if mainBoard == solvedBoard:
            msg = 'Solved!'
        """This is the main game loop, which constantly loops while the program is playing. In this loop, we display the board on the screen and also handle any input events from the player. The sliding variable will keep track of which direction we should slide the tiles. We have a separate variable for this so that we can treat input from the mouse and the keyboard the same way.

        We also want to display a text message at the top left corner of the window for various reasons. We will use the msg variable to store this string. If the board happens to be in the solved state, then we want the text message to be Solved!"""

        drawBoard(mainBoard, message=msg)
        """On each iteration we want to draw the current state of the board on the screen (along with any text message). Since the game loop runs 30 times a seconds (unless the computer is too slow or yo have changed the value in the FPS variable), we are constantly drawing the latest board to the screen."""

        if android is not None and android.check_pause():
            android.wait_for_resume()
        
        # Handle any events.
        for event in pygame.event.get():
            print event

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN and event.key == K_PAGEUP:
                terminate()
                
            if event.type == MOUSEBUTTONUP:
                spotClicked = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                """When the MOUSEBUTTONUP is created, we check if the mouse is currently over one of the tiles (otherwise we can ignore it.) The bulk of this is implemented inside our getSpotClicked() function. This function returns None if the mouse wasn't over a button, or it returns the color value of the button."""

                if spotClicked is not None:
                    spotx, spoty = spotClicked
                    """If getSpotClicked() did not return None, then this means the place on the window the player clicked was a spot (as opposed to somewhere in the margins)."""

                    blankx, blanky = getBlankPosition(mainBoard)
                    """We also need to find out where the blank spot currently is on the board. We'll get the xy coordinates of this spot from getBlankPosition()."""

                    if spotx == blankx + 1 and spoty == blanky:
                        sliding = LEFT
                    if spotx == blankx - 1 and spoty == blanky:
                        sliding = RIGHT
                    if spotx == blankx and spoty == blanky + 1:
                        sliding = UP
                    if spotx == blankx and spoty == blanky - 1:
                        sliding = DOWN
                    """Now we find out if the spot that the player clicked on is located next to the blank spot. We should slide a tile to the left if the blank spot is on its left, and slide the tile up if the blank space is above it, and so on."""
                else:
                    # check if the user clicked on one of the option buttons
                    if RESET_RECT.collidepoint(event.pos[0], event.pos[1]):
                        resetAnimation(mainBoard, seq)
                        seq = []
                        """Here we use the pygame.Rect object's collidepoint() method to find out if the x and y coordinates of the mouse click (which are in event.pos[0] and event.pos[1], respectively) are inside the rectangular area that the "reset" button occupies. If so, then we want to reset all the tiles back to their original configuration. We do this by passing resetAnimation() the sequence of moves made by the player so far (which is in the seq list). Of course, afterwards we'll want to set the seq list back to a blank list, since now the board is as though the player never made any moves at all."""
                    if NEW_RECT.collidepoint(event.pos[0], event.pos[1]):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        seq = []
                        """This code handles what happens when the user's mouse click was inside the "new game" button. Here we are going to start a brand new game, so we replace the board data structure stored in mainBoard and the sequence of moves to solve it in the solutionSeq list. We also want to reset the seq list since the player is starting a new game."""
                    if SOLVE_RECT.collidepoint(event.pos[0], event.pos[1]):
                        resetAnimation(mainBoard, solutionSeq + seq)
                        seq = []
                        """Here we check if the player has clicked on the "solve" button, in which case we do almost the same code as the "reset" button case. Except for this, instead of just reseting the sequence of steps the player has made (that is, the seq list) we reset the steps of the solution including the steps the player has made (solutionSeq + seq). This will reset the board back to the ordered starting board.

                        If the player wants a new puzzle, they will have to click the "new game" button to generate a new random puzzle."""

            if event.type == KEYUP:
                """The previous code checked what happens in the event that the user clicked the mouse (MOUSEBUTTONUP), while this code will handle what happens when the user presses a keyboard key. The key value that you can compare event.key to is stored in Pygame's own set of constants that have the format K_*, where the * is the letter of the key. In the case of the Esc key, it is K_ESCAPE.

                We need to call isValidMove() to make sure that the board is in a state where this move is allowed. Otherwise we would start sliding tiles off the board and cause bugs."""
                if (event.key == K_LEFT or event.key == K_a) and isValidMove(mainBoard, LEFT):
                    sliding = LEFT
                if (event.key == K_RIGHT or event.key == K_d) and isValidMove(mainBoard, RIGHT):
                    sliding = RIGHT
                if (event.key == K_UP or event.key == K_w) and isValidMove(mainBoard, UP):
                    sliding = UP
                if (event.key == K_DOWN or event.key == K_s) and isValidMove(mainBoard, DOWN):
                    sliding = DOWN
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_r:
                    resetAnimation(board, moves)

        if sliding:
            slideAnimation(mainBoard, sliding)
            makeMove(mainBoard, sliding)
            seq.append(sliding)
            """The sliding variable will not be None if the player specified (either through the keyboard or with the mouse) that we should slide the tiles. First we play the animation of the tile moving over, then we update the board data structure, and then we add this recent move to the list of moves the player has made in the seq list."""
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def terminate():
    """In order to terminate the program, we must call both pygame.quit() (to shut down the Pygame engine) and sys.exit() (to shut down the program.) Calling sys.exit() without calling pygame.quit() first probably won't harm anything, though it does give IDLE some problems if the user runs this program from it. It's just considered a graceful way to shut down the Pygame library."""
    pygame.quit()
    sys.exit()


def getStartingBoard():
    """This function creates a data structure that represents a state of the board. We will use a list of list of integers, where theBoard[2][3] would contain the integer that represents the spot on the board that is 3rd from the left and 4th from the top (remember, the indexes start at 0.) This mimics the coordinate system used by the screen, where the 0, 0 origin is at the top left corner.

    The integers represent the numbered tiles, so if theBoard[2][3] held the integer 12, then the "12" tile is located at the spot 3rd from the left and 4th from the top. The 0 integer will be used to represent the blank spot.

    Since this function creates a brand new board, we will want the tiles in order. So the data structure we want to create looks like:

        theBoard[0][0] == 1    theBoard[1][0] == 2    theBoard[2][0] == 3    theBoard[3][0] == 4
        theBoard[0][1] == 5    theBoard[1][1] == 6    theBoard[2][1] == 7    theBoard[3][1] == 8
        theBoard[0][2] == 9    theBoard[1][2] == 10   theBoard[2][2] == 11   theBoard[3][2] == 12
        theBoard[0][3] == 13   theBoard[1][3] == 14   theBoard[2][3] == 15   theBoard[3][3] == 0
    """

    counter = 1
    board = []
    for i in range(COLS):
        column = []
        """Because the inner lists represent each column, we have to add the integers in this pattern: first 1, 5, 9, 13, then second 2, 6, 10, 14, and so on.
        Notice that this follows the pattern of increasing by the number of columns, and then subtracts TODO """
        for j in range(ROWS):
            column.append(counter)
            counter += COLS
        board.append(column)
        counter -= COLS * (ROWS - 1) + COLS - 1

    board[COLS-1][ROWS-1] = 0
    return board


def generateNewPuzzle(numSlides):
    """This function takes a board that has its tiles in the starting position and performs several random slides on it to create the puzzle that the player needs to solve."""
    sequence = []
    """We'll want to keep track of the slides done when creating the new puzzle, so we'll store them in the sequence list."""
    board = getStartingBoard()
    drawBoard(board)
    pygame.display.update()
    time.sleep(0.5)
    """Note that we first draw the starting board to the screen by calling drawBoard() and then pygame.display.update(), and then pause the program for half of a second. This is to give the player enough to recognize the starting board before we start making random slides."""
    lastMove = None
    """We'll store the previous move made in the lastMove variable. This is so we don't end up doing a pointless set of slides, like sliding up and then immediately sliding down. But for the first time, we'll just store None in lastMove."""
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, animationSpeed=int(TILESIZE / 3), message='Generating new puzzle...')
        """We'll go through this loop however many times was specified in the integer variable numSlides. Each time, we get a random move and then perform the slide animation for that move."""
        makeMove(board, move)
        """Remember, the slideAnimation() function only does the graphics for the slide, it doesn't actually alter the board data structure. So we'll alter the data structure in the above line with the makeMove() function."""
        sequence.append(move)
        """We need to remember the series of random moves we did, so append the move to the sequence list."""
        lastMove = move
        """Store this move as the new value for lastMove."""
    return (board, sequence)
    """Return the board data structure as it now is (after all those random slides) and the sequence of slides that produced it. (We'll need the sequence info later if we want to solve the puzzle by undoing the slides."""


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
    """Making a move on the board is just a matter of swapping the value of the blank spot (the integer 0) with the value of the spot next to the space. We'll use the multiple assignment trick to swap the values. For example, if we had two variables named a and b, we could swap them with this line of code:

    a, b = b, a

    In the above code, we do the same thing, except we use values in the board data structure."""


def getLeftTopOfTile(tilex, tiley):
    """Remember from the comments in the getStartingBoard() function that we have two sets of coordinates in this program. The first set are the pixel coordinates, which on the x-axis ranges from 0 to WINDOWWIDTH - 1, and the y-axis ranges from 0 to WINDOWHEIGHT - 1.

    The other coordinate system is used to refer to the tiles on the game board. The upper left tile is at 0, 0. The x-axis ranges from 0 to COLS - 1, and the y-axis ranges from 0 to ROWS - 1."""
    left = XMARGIN + (tilex * TILESIZE) + (tilex - 1)
    top = YMARGIN + (tiley * TILESIZE) + (tiley - 1)
    return (left, top)


def isValidMove(board, move):
    """This function, give a board data structure and a proposed move direction (one of the UP, DOWN, LEFT, RIGHT values) will return True if the move is valid for the given board and False if it is not.

    Some of the moves when the blank spot is on the edge of the board are not valid. For example, if the blank spot is in the top left spot of the board, it is invalid to """
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)
    """This complicated-looking return statement is really straightforward. Technically the above four lines are just one line of code, but to make it readable, I've lined up the parts of the expression. The \ at the end of the line makes the Python interpreter consider the next line as a continuation of the current line.

    Let's look at the first part: (move == UP and blanky != len(board[0]) - 1)

    This means that if the move is UP, and the y coordinate of the blank spot is not len(board[0]) - 1 (that is, the bottom row), then this part of the expression evaluates to True.

    Notice that move can either be only one of the UP, DOWN, LEFT, and RIGHT values (we make sure it only ever has one of these values in our code). This will always make three of the four parts of the expression False. That means the remaining part MUST be True if the entire expression is to evaluate to True. Only one part of the four parts of the expression has to be True, because the four parts are all combined together with "or" operators.

    So, for example, if move is RIGHT, but the x coordiante of the blank spot (which is stored in blankx) is 0, then we couldn't possibly slide a tile to the right because the blank spot is on the left edge of the board. In that case, isValidMove() would return False."""


def getBlankPosition(board):
    for x in range(len(board[0])):
        for y in range(len(board)):
            """We use these nested for loops to iterate over every possible space in the board data structure."""
            if not board[x][y]:
                """Remember that we are using the integer value 0 to mark the blank spot, and the integer 0 maps to False. So the "not board[x][y]" condition here will be True for the blank spot."""
                return (x, y)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    """This function will draw a tile onto the MAINSURF surface. The calling code just supplies the x and y coordinates of the spot on the board (with tilex and tiley respectively) and the number to draw on the tile."""
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(MAINSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = FONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    MAINSURF.blit(textSurf, textRect)


def drawBoard(board, message=''):
    MAINSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        MAINSURF.blit(textSurf, textRect)

    for tilex in range(len(board[0])):
        for tiley in range(len(board)):
            if board[tilex][tiley]:
                """Just like in getBlankPosition(), we iterate through all the spaces in the board and the integer 0 is used to mark the blank spot. As long as we keep finding non-blank spots we want to call the drawTitle() function for that spot. str(board[tilex][tiley]) evaluates to a string of whatever the tile's number at that spot is."""
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = (COLS * TILESIZE) + (COLS - 1)
    height = (ROWS * TILESIZE) + (ROWS - 1)
    pygame.draw.rect(MAINSURF, BORDERCOLOR, (left - 5, top - 5, width + 9, height + 9), 4)
    """The four lines of code above draw the board around the board on the screen. First, we get the top left coordinates of the top left tile. Then we need to determine the width and height of the board in pixels. We can do this by multiplying the COLS by TILESIZE, and then adding COLS - 1 (to represent the single pixel gap in between each of the tiles, which will be one less than COLS). (The height is determined using ROWS instead of COLS.)

    Then we draw the border using pygame.draw.rect(). Notice that the left and top of the rectangle we are drawing are actually 5 pixels to the left and above the topleft corner of the top left tile. This is because we are going to make a thick border (4 pixels thick actually, which is what the 4 argument stands for.) So we need to offset where we start drawing so we don't draw the border over the tiles themselves. The same for the + 9 to the width and height. (5 of these pixels are to offset the -5 we had earlier, and the other 4 pixels to offset the thickness of the border.)"""

    MAINSURF.blit(RESET_SURF, RESET_RECT)
    MAINSURF.blit(NEW_SURF, NEW_RECT)
    MAINSURF.blit(SOLVE_SURF, SOLVE_RECT)
    """We want to draw the text of the three buttons (Reset Puzzle, New Puzzle, and Solve Puzzle) on the screen as well. The surface and rect object for each button are stored in the six global variables used above.

    Notice that we have not called the pygame.display.update() function, so drawBoard() doesn't actually update the image on the computer screen. We'll leave that to whatever code called drawBoard()."""


def slideAnimation(board, direction, animationSpeed=8, message=''):
    # This function does not check if the move is valid.

    """The slideAnimation() function works the following way: First we create a surface object the same size as the window, and draw the board as it would normally look on it. Then, we draw the background color over the tile that is going to slide. This makes the board look like it has two blank spots.

    This surface will be our "base" surface. To do the sliding animation, we will draw this base surface to the screen, and then draw the sliding tile on top of it. The sliding tile will be drawn in a slightly different position for each frame of this animation, so it looks like the tile is moving."""

    # prepare the base surface
    drawBoard(board, message=message)
    baseSurf = MAINSURF.copy()
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        """We will be looping to create the sliding animation. On each iteration of the loop, we draw the tile being slide a bit more than the last iteration."""
        checkForQuit()
        """While we are doing this animation, we still want to check if the player has tried to quit the program, so we call our checkForQuit() function."""
        if direction == UP:
            adjx = 0
            adjy = -i
        if direction == DOWN:
            adjx = 0
            adjy = i
        if direction == LEFT:
            adjx = -i
            adjy = 0
        if direction == RIGHT:
            adjx = i
            adjy = 0
        """We will draw the sliding tile in its normal position, except slightly adjusted by the value in the adjx and adjy variables. This will produce the "sliding" effect because the value in adjx or adjy increases on each iteration in the loop, causing the tile to appear to have slide more.

        Remember that a positive amount will move the tile to the right or down directions, but a negative amount will move it to the left and up directions.

        Note that we only want to slide along one axis, not both. This is why either adjx or adjy will be 0 no matter which of the UP, DOWN, LEFT, RIGHT directions we are moving."""

        MAINSURF.blit(baseSurf, (0, 0))
        """This draws the base surface to the screen, specifically with the top left corner of the base surface at the 0, 0 coordinates in the window."""
        drawTile(movex, movey, board[movex][movey], adjx, adjy)
        """Next we draw the sliding tile, slightly adjusted to give it that moving effect."""
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        """Then we call pygame.display.update() to update the screen, and call MAINCLOCK.tick(FPS) to pause the screen a little bit."""


def checkForQuit():
    """Sometimes we want to check the event queue for any QUIT events (or if the player has specifically pressed the Esc key to quit), but we don't care about any other events (such as mouse movements or clicks). By passing QUIT to the pygame.event.get() call, we return only QUIT events."""
    for event in pygame.event.get(QUIT):
        terminate()

    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        """We'll go through the events in the event queue again, this time only looking at KEYUP events (which happen when the player lets go of a keyboard key). If the key they pressed was the Esc key, we'll quit the program."""
        pygame.event.post(event)
        """If the key was not the escape key, then we want to return the KEYUP event to the event queue by calling pygame.event.post(). This ensures that we don't take out any, say, arrow key presses and then not handle them. The code in the main() function will later pick up these keyboard events, and properly handle them."""

    # Whenever we check for quit, we also want to check for an Android pause.
    if android is not None and android.check_pause():
        android.wait_for_resume()


def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    """We want to make sure that the random move this function returns is a valid move to make. So we'll create a list stored in the validMoves variable that contains all four direction values. Then we test each of the four directions to see if it is a valid move. If it is not a valid move, we'll remove that move from the validMoves list.

    For example, if the previous move was UP, then we don't want to return DOWN because that would make cancel out the last move."""
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    return random.choice(validMoves)
    """The random.choice() function will take a list or tuple value and return one of values in the list/tuple. We'll use this to randomly pick one of the remaining valid direction values."""


def getSpotClicked(board, x, y):
    """Remember from the comments in the getStartingBoard() function that we have two sets of coordinates in this program. The first set are the pixel coordinates, which on the x-axis ranges from 0 to WINDOWWIDTH - 1, and the y-axis ranges from 0 to WINDOWHEIGHT - 1.

    The other coordinate system is used to refer to the tiles on the game board. The upper left tile is at 0, 0. The x-axis ranges from 0 to COLS - 1, and the y-axis ranges from 0 to ROWS - 1."""
    for tilex in range(len(board[0])):
        for tiley in range(len(board)):
            """This set of nested for loops ensures that we run this block of code on each tile in the board. Note that we could have used COLS instead of len(board[0]) and ROWS instead fo len(board), but this way the range of integers we loop on depends on the board data structure rather than the ROWS and COLS global variables.

            This means we could call the getSpotClicked() function and pass board data structures besides the main one we draw on the screen. This makes the function more flexible to use."""
            left, top = getLeftTopOfTile(tilex, tiley)
            rectangle = pygame.Rect(left, top, TILESIZE, TILESIZE)
            """The above code creates a new pygame.Rect object which represents the area on the board that the tile covers."""
            if rectangle.collidepoint(x, y):
                return (tilex, tiley)
                """If the pixel coordinate (stored in the x and y parameters) is within the pygame.Rect object that represents the current tile we are iterating on, then the pygame.Rect object's collidepoint() method will return True. In that case, we want to return the coordinates of the tile that was clicked."""
    return None
    """If none of the tiles were clicked on, then the click must have been off the board entirely (or the blank spot was clicked) and we'll signify this by returning the None value."""


def resetAnimation(board, sequence):
    """Sometimes we will want to "undo" a sequence of slides, such as when we want to undo all the moves a player has made (which we do when the player clicks the "reset" button) or when we want to undo all the slides back to the starting, solved board (which we do when the player clicks on the "solve" button).

    First we will want to take the sequence of slides and reverse the order of them. Then, we want to do the opposite of the moves in the sequence (for example, go down if the move was UP)."""
    revSequence = sequence[:]
    """The [:] is a Python trick for copying the values in a list. Note that we cannot copy lists like we can copy values in other variables, because the variable does not contain the list but a reference to the list.

    More info on lists and list references can be found at http://inventwithpython.com/chapter10.html#ListReferences

    The [:] after sequence is technically a list slice. A slice is a sublist of the values in a list, much like an index just points to a single value in a list. For example, if we have this list:
        spam = [42, 10, 5, 100, 99]
    Then the index spam[2] refers to the integer 5 (remember, the indexes start a 0. 0 refers to the first item (42), 1 refers to the second item (10), 2 refers to the third itme (5), etc.)

    More info on slices and slicing can be found at http://inventwithpython.com/chapter9.html#SlicesandSlicing

    But a slice uses a colon to grab multiple values:
        eggs = spam[2:4]
    The above would put the list [5, 100] in the variable eggs. That is, it creates a new list and puts the values starting at (and including) index 2 and up to (but not including) the value at index 4. The integer before the colon is the starting index, and the integer after the colon is the ending index.

    If we leave out the first index in a slice, then Python interprets this as 0 (which is the first item.)
        bagels = spam[:4]
    The above line would put [42, 10, 5, 100] in the bagels variable.

    If we leave out the second index in a slice, then Python interprets this as meaning past the last index in the list:
        pancakes = spam[2:]
    The above line would put [5, 100, 99] in the pancakes variable.

    If we don't specify either index in a slice, then the ENTIRE list is copied. This is a quick way to copy a list, rather than just copying a list reference.
    """
    revSequence.reverse()
    """All list variables have a reverse() method that will flip the order of the items in a list, so we call that method here."""

    for move in revSequence:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        """For each move in the flipped (that is, reversed) sequence (revSequence) we want to get the opposite move. The opposite of UP is DOWN and the opposite of LEFT is RIGHT, so we set the oppositeMove variable accordingly."""

        slideAnimation(board, oppositeMove, animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)
        """Now we make the move by calling slideAnimation() (to display the sliding on the screen) and makeMove() (to actually update the board data structure). This is just like how we do in the main() and generateNewPuzzle() functions when the player makes a move."""


def makeText(text, color, bgcolor, top, left):
    textSurf = FONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    """The makeText() function has three lines of code that we call over and over again each time we want to create a bit of text. The first line creates a new pygame.Surface object with the text we provide drawn on it. Of course, we also have to provide the color of the text and the background color of the surface object. The True argument to the render() method specifies that we want to use anti-aliasing (which makes the text look a little less blocky.)

    There is more info on anti-aliasing at http://inventwithpython.com/chapter17.html#TherenderMethodforFontObjects

    Remember that the font size information is already stored in the pygame.font object stored in our global variable named FONT.

    In order to tell where we want this text to appear on the screen, we need to get a pygame.Rect object for this surface (this is what the "textRect = textSurf.get_rect()" line does) and set the top left corner to a specific position (this is what the "textRect.topleft = (top, left)" line does).
    """
    return (textSurf, textRect)


if __name__ == '__main__':
    main()
