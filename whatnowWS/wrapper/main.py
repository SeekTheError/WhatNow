import sys
sys.path.insert(0, '..')
import NYTimes
import WashingtonPost
from processing import maestro

"""
This file is made only for testing
"""
if __name__ == '__main__':
    NYTimes.wrapNYTimes('laden', 1)
    WashingtonPost.wrapWPost('laden', 1)
    maestro.analyzeAll()