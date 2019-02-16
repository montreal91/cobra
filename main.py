
import sys

import settings

from collections import deque
from typing import Deque

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import Point2

from helpers import gen_label_text
from helpers import load_object
from snake import Snake


class World(ShowBase):
    def __init__(self):
        super().__init__()

        self.disable_mouse()
        self._background = load_object(
            "background",
            pos=Point2(0, 0),
            scale=9000,
            depth=200,
            transparency=False
        )
        self._gameboard = load_object(
            "background",
            pos=Point2(0, 0),
            scale=39.5,
            depth=100,
            transparency=False
        )
        gen_label_text("ESC  : Quit", 0)
        gen_label_text("SPACE: Pause", 1)
        gen_label_text("R    : Restart", 2)
        self._score = gen_label_text(
            "", 0, left=False
        )

        self._bricks = deque()
        self._dot = load_object(
            "brick", pos=Point2(0, 0)
        )
        self._restart()
        self.accept("escape", sys.exit)
        self.accept("enter", self.restart)
        self.accept("arrow_up", self._turn, [settings.POS_Y])
        self.accept("arrow_down", self._turn, [settings.NEG_Y])
        self.accept("arrow_left", self._turn, [settings.NEG_X])
        self.accept("arrow_right", self._turn, [settings.POS_X])
        self.accept("space", self._tooggle_pause)
        self.accept("r", self._restart)

        self.period = settings.PERIOD
        self.pause = True

    def _game_loop(self, task):
        dt = task.time - task.last
        if not self._snake.alive:
            return task.done
        if self.pause:
            return task.cont
        elif dt >= self.period:
            task.last = task.time
            self._snake.move_forward()
            self._snake.check_state()
            self._update_snake()
            self._update_dot()
            self._update_score()
        return task.cont

    def _draw_snake(self):
        for point in self._snake.body:
            brick = load_object("brick", pos=Point2(point.real, point.imag))
            self._bricks.append(brick)

    def _update_snake(self):
        if len(self._snake.body) > len(self._bricks):
            new_head = self._dot
            self._make_dot()
            self._bricks.appendleft(new_head)

        for i in range(len(self._snake.body)):
            point = self._snake.body[i]
            brick = self._bricks[i]
            brick.setPos(point.real, settings.SPRITE_POS, point.imag)

    def _make_dot(self):
        self._dot = load_object(
            "brick", pos=Point2(self._snake.dot.real, self._snake.dot.imag)
        )

    def _update_dot(self):
        x, y = self._dot.getX(), self._dot.getZ()
        if (x, y) != self._snake.dot:
            self._dot.setPos(
                self._snake.dot.real, settings.SPRITE_POS, self._snake.dot.imag)

    def _update_score(self):
        self._score.setText(
            "Score: %s" % self._snake.get_score()
        )

    def _tooggle_pause(self):
        self.pause = not self.pause

    def _restart(self):
        self.pause = True
        for b in self._bricks:
            b.remove_node()
        self._snake = Snake(
            body=_make_default_body(),
            vector=settings.POS_X,
            dot=complex()
        )
        self._snake.gen_dot()
        self._bricks = deque()
        self._update_dot()
        self._draw_snake()
        taskMgr.remove("GameLoop")
        self._game_task = taskMgr.add(self._game_loop, "GameLoop")
        self._game_task.last = 0

    def _turn(self, direction: complex):
        if not self.pause:
            self._snake.turn(direction)


def _make_default_body():
    return [complex(-i, 1) for i in range(7, 10)]

if __name__ == '__main__':
    w = World()
    w.run()
