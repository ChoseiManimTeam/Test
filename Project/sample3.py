from manim import *
from manim_slides import Slide

class SlidesExample(Slide):
    def construct(self):
        self.next_slide(notes="Some introduction")
        square = Square(color=GREEN, side_length=2)

        self.play(GrowFromCenter(square))

        self.next_slide(notes="We now rotate the slide")

        self.play(Rotate(square, PI / 2))

        self.next_slide(notes="Bye bye")

        self.zoom(square)