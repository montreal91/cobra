

from collections import deque
from random import randrange

from settings import MAX_X
from settings import MAX_Y


class Snake:
    def __init__(self, body, vector, dot):
        self.body = deque(body)
        self.vector = vector
        self.dot = dot
        self.alive = True
        self.init_len = len(self.body)
        self._previous_step = self.vector

    def check_state(self):
        head = self.body[0]
        if self.body.count(head) > 1:
            self.alive = False
        elif not -MAX_X <= head.real <= MAX_X:
            self.alive = False
        elif not -MAX_Y <= head.imag <= MAX_Y:
            self.alive = False

    def move_forward(self):
        head = self.body[0]
        next_brick = complex(
            head.real + self.vector.real, head.imag + self.vector.imag
        )
        self.body.appendleft(next_brick)
        if head == self.dot:
            self.gen_dot()
        if next_brick != self.dot:
            self.body.pop()
        self._previous_step = self.vector

    def turn(self, direction):
        if self._previous_step + direction != 0:
            self.vector = direction

    def gen_dot(self):
        while self.dot in self.body:
            self.dot = complex(
                randrange(- MAX_X, MAX_X),
                randrange(-MAX_Y, MAX_Y)
            )

    def get_score(self):
        return len(self.body) - self.init_len
