'''
Limesqueezer
========================================================================

Lossy compression tools for smooth data series.

Recommended abbreviation is 'ls'

import limesqueezer as ls
'''

__version__ = '1.0.8'

import sys
import pathlib

sys.path.insert(1,str(pathlib.Path(__file__).parent.absolute()))

from .API import *

helpstring = 'No arguments given'

if len(sys.argv)==1:
    print(__doc__)
    print(helpstring)
    exit()
elif sys.argv[1] == 'debug':
    import plotters
    debugplot = plotters.Debug(errorf=sys.argv[2] if len(sys.argv)>2 else 'maxmaxabs',
                                fitf = sys.argv[3] if len(sys.argv)>3 else 'poly1')
    debugplot.run()
    input()