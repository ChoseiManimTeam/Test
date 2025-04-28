from manim import *

class UsingCircumscribe(Scene):
    def construct(self):
        lbl = Tex(r"Circum-\\scribe").scale(2)
        self.add(lbl)

        # 通常の囲み
        self.play(Circumscribe(lbl))
        # 円で囲む
        self.play(Circumscribe(lbl, Circle))
        # フェードアウト付き
        self.play(Circumscribe(lbl, fade_out=True))
        # 時間幅を長くする
        self.play(Circumscribe(lbl, time_width=2))
        # 円形、フェードイン付き
        self.play(Circumscribe(lbl, Circle, True))
