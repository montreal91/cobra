
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Point2
from panda3d.core import Point3
from panda3d.core import TextNode

from settings import SPRITE_POS


def gen_label_text(text, i, left=True):
    label = OnscreenText(text=text)
    label["fg"] = (0.148, 0.176, 0.105, 1)
    label["align"] = TextNode.ALeft
    label["scale"] = 0.06
    label["font"] = loader.load_font('data/fonts/FreeMonoBold.ttf')
    if left:
        label["pos"] = (-1.3, 0.95 - 0.06 * i)
    else:
        label["pos"] = (0.95, 0.95 - 0.06 * i)
    return label


def load_object(
        tex=None, pos=None, depth=SPRITE_POS, scale=1, transparency=True
):
    obj = loader.load_model("data/models/plane")
    obj.reparent_to(camera)
    obj.set_pos(Point3(pos.getX(), depth, pos.getY()))
    obj.set_scale(scale)
    obj.set_bin("unsorted", 0)
    obj.set_depth_test(False)
    if transparency: obj.set_transparency(1)
    if tex:
        tex = loader.load_texture("data/sprites/"+tex+".png")
        obj.set_texture(tex, 1)
    return obj
