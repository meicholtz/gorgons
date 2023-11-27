# utils.py
# Utility functions for Gorgons.
#
#
# Author: Matthew Eicholtz
# Inspired by: http://kyleburke.info/DB/combGames/gorgons.html

import subprocess

def getversion():
    """Retrieve the current git hash to use as a 'version' number."""
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

def test():
	"""Test utility functions for errors."""
	print('\nGORGONS')
	print('=' * 30)
	print('Testing utility functions...')
	print(f'    Version: {getversion()}')

if __name__ == "__main__":
    test()