# -*- coding: utf-8 -*- 

from settings       import *
from collections    import deque
from random         import randrange

class Snake( object ):
    def __init__( self, body=[(0, 0), (1, 0), (2, 0)], vector=POS_X, dot=(0, 0) ):
        object.__init__( self )
        self.body           = deque( body )
        self.vector         = vector
        self.dot            = dot
        self.alive          = True
        self.init_len       = len( self.body )

    def check_state( self ):
        head = self.body[0]
        if self.body.count( head ) > 1: self.alive = False #return False
        elif head[X] < -MAX_X or head[X] > MAX_X: self.alive = False #return False
        elif head[Y] < -MAX_Y or head[Y] > MAX_Y: self.alive = False #return False

    def move_forward( self ):
        head = self.body[0]
        next = ( head[X] + self.vector[X], head[Y] + self.vector[Y] )
        self.body.appendleft( next )
        if head == self.dot:
            self.gen_dot( )
        if next != self.dot:
            self.body.pop( )

    def turn ( self, direction ):
        scal_prod   = self.vector[X] * direction[X] + self.vector[Y] * direction[Y]
        if scal_prod == 0:
            self.vector = direction

    def gen_dot( self ):
        while self.dot in self.body:
            self.dot    = ( randrange( - MAX_X, MAX_X ), randrange( -MAX_Y, MAX_Y ) )

    def get_score( self ):
        return len( self.body ) - self.init_len
