# utils.py
# Utility functions for Gorgons.
#
# Author: Matthew Eicholtz
# Inspired by: http://kyleburke.info/DB/combGames/gorgons.html

from graphics import *
import pdb
import subprocess

ROOT = os.path.dirname(os.path.realpath(__file__))
COLORS = { # dictionary of colors relevant to the game user interface
	'empty': '#ffffff',
	'pre-stone': '#000000',
	'stone': '#808080',
	'active': '#ffff00',
	'outline': '#000000',
	'text': '#000000'
	}
FONT = 14 # font size for instructions
GORGONS = { # dictionary of filenames for gorgon sprites
	'red': os.path.join(ROOT, 'img', 'gorgon_red50.png'),
	'blue': os.path.join(ROOT, 'img', 'gorgon_blue50.png')
	}
HEADER = 30 # space for instructions at the top of the board, in pixels
MARGIN = 15 # margin on side of the board, in pixels
SIZE = 50 # size of each space on the board, in pixels

def convert_click(board, x, y):
    '''Determine which space on the board was clicked by the mouse.
    
    Parameters
    ----------
    board : int
        Number of rows and columns on the board.
    x : int
        The x-coordinate of the mouse click.
    y : int
        The y-coordinate of the mouse click.

    Returns
    -------
    row : int
        The corresponding row of the mouse click (0-indexed).
    col : int
        The corresponding column of the mouse click (0-indexed).
    '''
    row = (y - MARGIN - HEADER) // SIZE
    col = (x - MARGIN) // SIZE

    # Check for out-of-bounds error
    if not (0 <= row < board):
    	row = -1
    if not (0 <= col < board):
    	col = -1

    return row, col

def getversion():
    """Retrieve the current git hash to use as a 'version' number."""
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

def guisetup(board=9, blue=2, red=2):
    '''Create the graphical user interface for the game.
    
    Parameters
    ----------
    board : int
        Number of rows and columns on the board.
    blue : int
        Number of blue gorgons in the game.
    red : int
        Number of red gorgons in the game.

    Returns
    -------
    gui : GraphWin object
        The graphics window object containing all of the necessary UI elements.
    '''
    # Input checking
    if blue > board // 2:
    	raise Exception(f'The number of blue gorgons ({blue}) cannot exceed half the board size ({board // 2})')
    if red > board // 2:
    	raise Exception(f'The number of red gorgons ({red}) cannot exceed half the board size ({board // 2})')

    # Make game window
    wid = board * SIZE + MARGIN * 2
    hei = board * SIZE + MARGIN * 2 + HEADER
    gui = GraphWin("Gorgons", wid, hei)

    # Add board
    for row in range(board):
    	for col in range(board):
    		x1 = MARGIN + col * SIZE
    		y1 = HEADER + MARGIN + row * SIZE
    		x2 = x1 + SIZE
    		y2 = y1 + SIZE
    		cell = Rectangle(Point(x1, y1), Point(x2, y2))
    		cell.setFill(COLORS['empty'])
    		cell.setOutline(COLORS['outline'])
    		# cell.setWidth(1)
    		cell.draw(gui)

    # Set middle of the board to stone (this add some complexity to the game strategy)
    if board % 2 == 0: # even boards have 2x2 middle section
    	middle = board // 2 - 1
    	index = middle * (board + 1) # linear index of (first) middle cell in the list of Rectangle objects
    	gui.items[index].setFill(COLORS['stone'])
    	gui.items[index + 1].setFill(COLORS['stone'])
    	gui.items[index + board].setFill(COLORS['stone'])
    	gui.items[index + board + 1].setFill(COLORS['stone'])
    else: # odd boards have 1x1 middle section
    	middle = board // 2
    	index = middle * (board + 1) # linear index of middle cell in the list of Rectangle objects
    	gui.items[index].setFill(COLORS['stone'])

    # Add red gorgons (starting from top-left corner, i.e. index=0)
    for i in range(red):
    	row = 0
    	col = 2 * i
    	x = MARGIN + SIZE * col + SIZE // 2
    	y = HEADER + MARGIN + SIZE * row + SIZE // 2
    	gorgon = Image(Point(x, y), GORGONS['red'])
    	gorgon.draw(gui)

    # Add blue gorgons (starting from bottom-left corner shifted one to the right, i.e. index=73 on a standard 9x9 board)
    for i in range(blue):
    	row = board - 1
    	col = 2 * i + 1
    	x = MARGIN + SIZE * col + SIZE // 2
    	y = HEADER + MARGIN + SIZE * row + SIZE // 2
    	gorgon = Image(Point(x, y), GORGONS['blue'])
    	gorgon.draw(gui)

    # Add text instructions
    instructions = Text(Point(wid // 2, (HEADER + MARGIN) // 2), "Blue goes first.")
    instructions._reconfig("anchor", "center")
    instructions.setSize(FONT)
    instructions.draw(gui)

    # Store relevant parameters in the gui object
    params = {key: value for key, value in globals().items() if key.isupper() and '_' not in key}
    gui.items.append(params)

    return gui

def test():
	"""Test utility functions for errors."""
	print('\nGORGONS')
	print('=' * 30)
	print('Testing utility functions...')
	print(f'    Version: {getversion()}')
	print(f'    Making standard board...')
	gui = guisetup()
	while True:
		key = gui.checkKey()
		if key:
			if key == "Escape" or key == "Ctrl+e":  # exit game
				break
			elif key == 'd':
				pdb.set_trace()

if __name__ == "__main__":
    test()