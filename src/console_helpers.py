# -*- coding: utf-8 -*-
"""
Created on Sun May 13 17:45:24 2018 by Misha

TODO: Add module docstring
"""

# Py2-proofing
from __future__ import print_function

class Tkinter_Element_Fake(object):
    
    def __init__(self, root, *args, **kwargs):
        self._root = root
        
    def _show(self):
        pass

class Tkinter_Label_Fake(Tkinter_Element_Fake):
    
    def __init__(self, root, labeltext):
        super().__init__(self, root)
        self._label = labeltext
        
    def config(self, text=None):
        self._label = text or self._label
    
    def _show(self):
        print(self._label, end='\r')

class Tkinter_Entry_Fake(Tkinter_Element_Fake):
    
    def __init__(self, root, width=None):
        super().__init__(self, root)
        self._width = width
        self._last_input = None
        self._default = ''
    
    def get(self):
        inp = None
        if self._last_input is not None:
            inp = input("Enter input (blank for previous) > {}".format(
                    self.default)).strip()
            if not inp:
                inp = self._last_input
        else:
            inp = input("Enter input > {}".format(self._default)).strip()
        
        self._last_input = inp
        return inp
    
    def delete(self, index, end):
        if index == 0 and end == 'end':
            self._default = ''
        else:
            raise NotImplemented("not sure what to do...")
    
    def insert(self, index, text):
        if index == 0:
            self._default = text
        else:
            raise NotImplemented("not sure what to do...")
        