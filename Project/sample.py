from manim import *

class MovingSquareWithUpdaters(Scene):
    def construct(self):
        title = Text("What is").to_edge(UP)
        formula = MathTex(r"(1,2,3) * (4,5,6)").scale(1.5).next_to(title, DOWN)
        self.add(title, formula)
        square1 = VGroup(*[Square().scale(0.6) for i in range(3)]).arrange(RIGHT, buff=0)
        int1 = Integer(1).scale(1.5).move_to(group1[0])
        nums1 = VGroup(*[Integer(i+1).scale(1.5).move_to(group1[i]) for i in range(3)])
        self.add(square1, nums1)
