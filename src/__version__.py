# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 15:11:57 2018

@author: Misha
"""

__major__ = 2
__minor__ = 0
__patch__ = 0

__version__ = '.'.join(map(str, [__major__, __minor__, __patch__]))
__int_version__ = int(''.join(map(str, [__major__, __minor__, __patch__])))

__author__ = "Michael Turnbull"
__author_email__ = "mishaturnbull@gmail.com"

__url__ = "https://github.com/mishaturnbull/PySpeedTest"

def is_version_greater(ver1, ver2, safe=True):
    """
    Assumes ver1 and ver2 are both of the form a.b.c
    """
    maj1, min1, pat1 = [int(i) for i in ver1[1:].split('-')[0].split('.')]
    maj2, min2, pat2 = [int(i) for i in ver2[1:].split('-')[0].split('.')]

    if safe:
        prerels = ['alpha', 'beta', 'pre', 'test']
        if any(p in ver1 for p in prerels):
            return False

    if maj1 > maj2:
        return True
    if min1 > min2:
        return True
    if pat1 > pat2:
        return True
    return False
