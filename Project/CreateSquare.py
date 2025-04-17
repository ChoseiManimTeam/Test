from manim import *

class DoubleSquare(Scene):
    def construct(self):
        square1 = Square(color = BLUE)                # Mobject機能
        square2 = Square(color = RED)                 # Mobject機能
        circle = Circle(color = GREEN)                # Mobject機能

        square1.move_to([2, 2, 0])                    # Mobject機能
        square2.move_to([-2, 2, 0])                   # Mobject機能

        anim1 = square1.animate.move_to([-2, -2, 0])  # Animation機能
        anim2 = square2.animate.move_to([2, -2, 0])   # Animation機能
        animEnd = FadeOut(square1, square2)           # Animation機能

        self.add(circle)                              # Scene機能
        self.play(anim2)                       # Scene機能
        self.play(animEnd)                            # Scene機能
