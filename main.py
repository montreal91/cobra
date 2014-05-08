# -*- coding: utf-8 -*- 

import sys
import snake

from panda3d.core                   import Point2

from direct.showbase.ShowBase       import ShowBase
from direct.task.Task               import Task

from settings                       import *
from helpers                        import genLabelText, loadObject

class World( ShowBase ):
    def __init__ ( self ):
        ShowBase.__init__( self )

        self.disableMouse( )
        self.snake          = snake.Snake( body=[ (-7, 1), (-8, 1), (-9, 1) ], dot=(-7, 1) )
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

        self.game_task      = taskMgr.add( self.game_loop, "GameLoop" )
        self.game_task.last = 0
        self.period         = 0.15

    def game_loop( self, task ):
        dt = task.time - task.last
        if not self.snake.alive: 
            print len( self.bricks )
            return task.done
        if dt >= self.period:
            task.last = task.time
            self.snake.move_forward( )
            self.snake.check_state( )
            self.draw_snake( )
            # self.draw_bricks( )
            self.update_score( )
            return task.cont
        else:
            return task.cont


    def draw_snake( self ):  
        if self.bricks:
            for brick in self.bricks:
                brick.removeNode( )

        for point in self.snake.body:
            brick = loadObject( "brick", pos=Point2( point[ X ], point[ Y ] ) )
            self.bricks.append( brick )
        dot = loadObject( "brick", pos=Point2( self.snake.dot[ X ], self.snake.dot[ Y ] ) )
        self.bricks.append( dot )

    def update_score ( self ):
        if self.score:
            self.score.removeNode( )
        self.score = genLabelText( "Score: %s" % self.snake.get_score( ), 1 )

w   = World( )
w.run( )
