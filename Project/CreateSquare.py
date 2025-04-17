from manim import *

class CircleMove(Scene):
    def construct(self):
        circle = Circle(color = RED)  # Mobject機能
        circle.move_to([-2, 2, 0])     # Mobject機能

        animFirst = Create(circle)     # Animation機能
        animMiddle = circle.animate.move_to([-2, -2, 0]).set_color(GREEN)
        animEnd = FadeOut(circle)      # Animation機能

        self.play(animFirst)           # Scene機能
        self.play(animMiddle)          # Scene機能
        self.play(animEnd)             # Scene機能
