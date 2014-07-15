import sys
import os

ts_dir = os.path.dirname(os.path.realpath(__file__)) + '/ts'
sys.path.append(ts_dir)

from ts.settings import *