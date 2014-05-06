# -*- coding: utf-8 -*- 

import sys
import snake
import time

from panda3d.core                   import Point2

from direct.showbase.ShowBase       import ShowBase
from direct.task.Task               import Task

from settings                       import *
from helpers                        import genLabelText, loadObject

class World( ShowBase ):
    def __init__ ( self ):
        ShowBase.__init__( self )

        self.disableMouse( )
        self.snake          = snake.Snake( body=[ (-7, 1), (-8, 1), (-9, 1) ] )
        self.snake.gen_dot( )

        self.background     = loadObject( "background", scale=9000, depth=200, transparency=False )
        self.gameboard      = loadObject( "background", scale=39.5, depth=100, transparency=False )
        self.escapeText     = genLabelText( "ESC: Quit", 0 )
        self.score          = genLabelText( "Score: %s" % self.snake.get_score( ), 1 )
        self.bricks         = [ ]

        self.accept( "escape",      sys.exit )
        self.accept( "enter",       self.restart )
        self.accept( "arrow_up",    self.snake.turn, [ POS_Y ] )
        self.accept( "arrow_down",  self.snake.turn, [ NEG_Y ] )
        self.accept( "arrow_left",  self.snake.turn, [ NEG_X ] )
        self.accept( "arrow_right", self.snake.turn, [ POS_X ] )

        self.taskMgr.add( self.game_loop, "GameLoop" )

    def game_loop( self, task ):
        if not self.snake.alive: 
            return task.done
        else:
            time.sleep( 0.1 ) # cruft
            self.snake.move_forward( )
            self.snake.check_state( )
            self.draw_snake( )
            self.update_score( )
            return task.cont

    def draw_snake( self ):  
        if self.bricks:
            for brick in self.bricks:
                brick.removeNode( )
        for y in xrange( - MAX_Y, MAX_Y + 1 ):
            for x in xrange( - MAX_X, MAX_X + 1 ):
                if (x, y) in self.snake.body or (x, y) == self.snake.dot:
                    brick = loadObject("brick", pos=Point2( x, y ) )
                    self.bricks.append( brick )

    def update_score ( self ):
        if self.score:
            self.score.removeNode( )
        self.score = genLabelText( "Score: %s" % self.snake.get_score( ), 1 )


w   = World( )
run( )
