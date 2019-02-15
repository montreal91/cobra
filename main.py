
import sys

import snake
import settings

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import Point2

from helpers import gen_label_text
from helpers import load_object
from collections import deque


class World(ShowBase):
    def __init__(self):
        super().__init__()

        self.disable_mouse()
        self.snake = snake.Snake(
            body=[complex(-7, 1), complex(-8, 1), complex(-9, 1)],
            dot=complex(-7, 1),
            vector=settings.POS_X,
        )
        self.snake.gen_dot()

        self.background = load_object(
            "background",
            pos=Point2(0, 0),
            scale=9000,
            depth=200,
            transparency=False
        )
        self.gameboard = load_object(
            "background",
            pos=Point2(0, 0),
            scale=39.5,
            depth=100,
            transparency=False
        )
        self.escape_text = gen_label_text("ESC  : Quit", 0)
        self.pause_text = gen_label_text("SPACE: Pause", 1)
        self.score = gen_label_text(
            "SCORE: %s" % self.snake.get_score(), 0, left=False
        )

        self.bricks = deque()
        self.make_dot()

        self.draw_snake()
        self.accept("escape", sys.exit)
        self.accept("enter", self.restart)
        self.accept("arrow_up", self.snake.turn, [settings.POS_Y])
        self.accept("arrow_down", self.snake.turn, [settings.NEG_Y])
        self.accept("arrow_left", self.snake.turn, [settings.NEG_X])
        self.accept("arrow_right", self.snake.turn, [settings.POS_X])
        self.accept("space", self.tooggle_pause)

        self.game_task = taskMgr.add(self.game_loop, "GameLoop")
        self.game_task.last = 0
        self.period = 0.15
        self.pause = False

    def game_loop(self, task):
        dt = task.time - task.last
        if not self.snake.alive:
            return task.done
        if self.pause:
            return task.cont
        elif dt >= self.period:
            task.last = task.time
            self.snake.move_forward()
            self.snake.check_state()
            self.update_snake()
            self.update_dot()
            self.update_score()
        return task.cont

    def draw_snake(self):
        for point in self.snake.body:
            brick = load_object("brick", pos=Point2(point.real, point.imag))
            self.bricks.append(brick)

    def update_snake(self):
        if len(self.snake.body) > len(self.bricks):
            new_head = self.dot
            self.make_dot()
            self.bricks.appendleft(new_head)

        for i in range(len(self.snake.body)):
            point = self.snake.body[i]
            brick = self.bricks[i]
            brick.setPos(point.real, settings.SPRITE_POS, point.imag)

    def make_dot(self):
        self.dot = load_object(
            "brick", pos=Point2(self.snake.dot.real, self.snake.dot.imag)
        )

    def update_dot(self):
        x, y = self.dot.getX(), self.dot.getZ()
        if (x, y) != self.snake.dot:
            self.dot.setPos(
                self.snake.dot.real, settings.SPRITE_POS, self.snake.dot.imag)

    def update_score(self):
        self.score.setText(
            "Score: %s" % self.snake.get_score()
        )

    def tooggle_pause(self):
        self.pause = not self.pause

w = World()
w.run()
