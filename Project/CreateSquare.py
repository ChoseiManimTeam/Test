from manim import *

class CreateSquare(Scene):
    def construct(self):
        square = Square()
        createAnim = Create(square)
        self.play(createAnim)
