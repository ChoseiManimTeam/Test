from manim import *

class CreateSquare(Scene):
    def construct(self):
        self.play(Create(Square()))

