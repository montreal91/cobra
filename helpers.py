# -*- coding: utf-8 -*- 

from settings                   import *

from panda3d.core               import Point2, Point3
from panda3d.core               import TextNode

from direct.gui.OnscreenText    import OnscreenText

def genLabelText( text, i ):
    return OnscreenText( text = text, pos = ( -1.3, .95-.05*i ), fg=( 1,1,0,1 ), align = TextNode.ALeft, scale = .05 )

def loadObject( tex=None, pos=Point2(0,0), depth=SPRITE_POS, scale=1, transparency=True ):
    obj = loader.loadModel( "models/plane" )
    obj.reparentTo( camera )
    obj.setPos( Point3( pos.getX( ), depth, pos.getY( ) ) )
    obj.setScale( scale )
    obj.setBin( "unsorted", 0 )
    obj.setDepthTest( False )
    if transparency: obj.setTransparency( 1 )
    if tex:
        tex = loader.loadTexture("sprites/"+tex+".png") 
        obj.setTexture(tex, 1)
    return obj
