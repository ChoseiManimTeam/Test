from manim import *

class MovingIntegralArea(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        plane = NumberPlane(
            x_range=[-1, 6],
            y_range=[-4, 16, 2],
            x_length=12,
            y_length=8
        ).add_coordinates()

        graph = plane.plot(lambda x: (x-2)*(x-2-2)*(x+2-2))

        def updater(mobject):
            mobject.move_to(plane.i2gp(tracker.get_value(), graph))

        dot = Dot()
        dot.add_updater(updater)

        area = always_redraw(lambda: plane.get_area(
            graph,
            x_range=(0, tracker.get_value()),
            opacity=0.7))
        

        self.add(plane, graph, dot, area)
        self.play(tracker.animate.set_value(5), run_time=4)
        self.wait()