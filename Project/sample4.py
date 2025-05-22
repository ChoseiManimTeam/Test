from manim import *

class SimpleExample(Scene):
    def construct(self):
        question = Text("What is")
        conv = MathTex("(1, 2, 3) * (4, 5, 6)")
        group = VGroup(question, conv).arrange(DOWN).to_edge(UP)

        self.play(
            Write(question, run_time=1.5),
            FadeIn(conv, shift=0.5 * DOWN, time_span=(0.5, 1.5)),
        )
        self.wait()

        top_row = VGroup(*[Square(0.75) for _ in range(3)]).arrange_in_grid(rows=1, cols=3, buff=0)
        top_row.set_stroke(GREY_B, 2).set_fill(GREY_E, 1)

        low_row = top_row.copy()

        for row, values in ((top_row, range(1, 4)), (low_row, range(4, 7))):
            for idx, (value, square) in enumerate(zip(values, row)):
                value_label = Integer(value)
                value_label.move_to(square)
                square.value_label = value_label
                square.value = value
                square.index = idx
                square.add(value_label)

        VGroup(top_row, low_row).arrange(RIGHT, buff=LARGE_BUFF)

        self.play(
            TransformMatchingShapes(conv[1:6:2].copy(), top_row),
            TransformMatchingShapes(conv[9:14:2].copy(), low_row),
        )
        self.wait()

        self.add_block_labels(top_row, "a", BLUE)
        self.add_block_labels(low_row, "b", RED)

        top_row.generate_target()
        low_row.generate_target()

        low_row.target.rotate(PI)
        for sq in low_row.target:
            sq.value_label.rotate(PI)
            sq.label.rotate(PI)

        top_row.target.center()
        low_row.target.next_to(top_row.target, DOWN, MED_LARGE_BUFF)

        conv_result = np.convolve([1, 2, 3], [4, 5, 6])
        rhs_tokens = ["=", R"\big("]
        for k in conv_result:
            rhs_tokens.append(str(k))
            rhs_tokens.append(",")
        rhs_tokens[-1] = R"\big)"
        rhs = MathTex(*rhs_tokens)
        rhs[2::2].set_color(YELLOW)

        conv.generate_target()
        VGroup(conv.target, rhs).arrange(RIGHT, buff=0.2).next_to(top_row, UP, buff=2)

        self.play(
            LaggedStart(
                MoveToTarget(top_row),
                MoveToTarget(low_row, path_arc=PI),
                MoveToTarget(conv),
                Write(VGroup(*rhs[:2], rhs[-1])),
                FadeOut(question, shift=UP),
            )
        )
        self.wait()

        def get_row_shift(n):
            min_idx = low_row[0].index
            max_idx = top_row[-1].index
            max_sum = min_idx + max_idx
            if n <= max_sum:
                x_shift = top_row[n - 2 * min_idx].get_x() - low_row[0].get_x()
            else:
                x_shift = top_row[-1].get_x() - low_row[n - max_sum].get_x()
            return low_row.animate.shift(x_shift * RIGHT)

        def get_aligned_pairs(n):
            return VGroup(
                *(
                    VGroup(m1, m2)
                    for m1 in top_row
                    for m2 in low_row
                    if m1.index + m2.index == n
                )
            )

        c_labels = VGroup()
        for n in range(len(conv_result)):
            self.play(get_row_shift(n))

            pairs = get_aligned_pairs(n)

            expr      = VGroup()
            symbols   = VGroup()
            label_cpy = VGroup()

            for m1, m2 in pairs:
                f1 = m1.value_label.copy().set_angle(0)
                f2 = m2.value_label.copy().set_angle(0)

                pair = VGroup(f1, f2).arrange(RIGHT, buff=MED_SMALL_BUFF)

                pair.next_to(expr, RIGHT, SMALL_BUFF)

                dot  = MathTex(r"\dot").move_to(pair)
                plus = MathTex("+").next_to(pair, RIGHT, SMALL_BUFF)

                expr.add(pair, dot, plus)
                symbols.add(dot, plus)
                label_cpy.add(pair)

            symbols[-1].scale(0, about_point=symbols[-2].get_right())
            label_pairs = VGroup(*(VGroup(m1.value_label, m2.value_label) for m1, m2 in pairs))
            c_label = MathTex(f"c_{n}", font_size=30, color=YELLOW).next_to(rhs[2 * n + 2], UP)
            rects = VGroup(*(SurroundingRectangle(lp, corner_radius=0.2).set_stroke(YELLOW, 1) for lp in label_pairs))

            expr.next_to(rects, UP, LARGE_BUFF)

            self.play(
                FadeIn(rects),
                LaggedStart(
                    *(
                        TransformFromCopy(orig_pair, copy_pair)
                        for orig_pair, copy_pair in zip(
                            (VGroup(m1.value_label, m2.value_label) for m1, m2 in pairs),
                            label_cpy
                        )
                    ),
                    lag_ratio=0.5,
                ),
                Write(symbols),
            )

            self.play(
                FadeTransform(expr.copy(), rhs[2 * n + 2]),
                FadeIn(c_label),
            )
            if n < len(conv_result) - 1:
                self.play(Write(rhs[2 * n + 3]))
            self.play(FadeOut(expr), FadeOut(rects))
            c_labels.add(c_label)

        self.play(FadeOut(c_labels))

        equation = VGroup(conv, rhs)
        values1 = VGroup(*(sq.value_label for sq in top_row)).copy()
        values2 = VGroup(*(sq.value_label for sq in low_row)).copy()

        grid = VGroup(*[Square(1.0) for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=0)
        grid.set_stroke(WHITE, 2).set_fill(GREY_E, 1).move_to(DL)

        self.play(
            Write(grid, time_span=(0.5, 2.0)),
            LaggedStart(
                *(
                    v.animate.next_to(sq, UP, buff=0.2)
                    for v, sq in zip(values1, grid[:3])
                ),
                *(
                    v.animate.next_to(sq, LEFT, buff=0.2)
                    for v, sq in zip(values2, grid[0::3])
                ),
                run_time=2,
            ),
            *(
                MaintainPositionRelativeTo(block, value)
                for row, vals in ((top_row, values1), (low_row, values2))
                for block, value in zip(row, vals)
            ),
            FadeOut(top_row),
            FadeOut(low_row),
            equation.animate.center().to_edge(UP),
        )

        products = VGroup()
        diag_groups = [VGroup() for _ in range(5)]

        for n, sq in enumerate(grid):
            i, j = divmod(n, 3)
            v1, v2 = values1[j], values2[i]
            prod = Integer(v1.get_value() * v2.get_value()).match_height(v1).move_to(sq)
            prod.factors = (v1, v2)
            sq.product = prod
            products.add(prod)
            diag_groups[i + j].add(prod)

        products.set_color(GREEN)

        self.play(
            LaggedStart(
                *(
                    ReplacementTransform(factor.copy(), prod)
                    for prod in products
                    for factor in prod.factors
                ),
                lag_ratio=0.1,
            )
        )
        self.wait()

        products.rotate(PI / 4)
        ovals = VGroup()
        radius = 0.3
        for diag in diag_groups:
            oval = SurroundingRectangle(diag, buff=0.19)
            oval.stretch_to_fit_width(2 * radius).set_stroke(YELLOW, 2).round_corners(radius)
            ovals.add(oval)
        VGroup(products, ovals).rotate(-PI / 4)
        ovals[0].become(Circle(radius=radius).match_style(ovals[0]).move_to(products[0]))

        arrow_targets = VGroup(
            *(
                Vector(0.5 * UP).next_to(rhs[2 * i + 2], DOWN, buff=SMALL_BUFF)
                for i in range(len(conv_result))
            )
        ).set_color(YELLOW)

        curr_arrow = arrow_targets[0].copy().shift(0.5 * DOWN).set_opacity(0)

        for n, (oval, arrow) in enumerate(zip(ovals, arrow_targets)):
            self.play(
                Create(oval),
                ovals[:n].animate.set_stroke(opacity=0.25),
                Transform(curr_arrow, arrow),
            )
            self.wait(0.5)

        self.play(ovals.animate.set_stroke(opacity=0.25), FadeOut(curr_arrow))
        self.wait()

        grid_group = VGroup(grid, values1, values2, products, ovals)

        poly_eq = MathTex(
            r"\left({1} + {2x} + {3x^2}\right)",
            r"\left({4} + {5x} + {6x^2}\right)",
            r"=\,{4} + {13}x + {28}x^2 + {27}x^3 + {18}x^4",
            tex_to_color_map={
                "{1}": YELLOW, "{2x}": YELLOW, "{3x^2}": YELLOW,
                "{4}": YELLOW, "{5x}": YELLOW, "{6x^2}": YELLOW,
                **{f"{{{n}}}": YELLOW for n in (4, 13, 28, 27, 18)},
            },
        )
        poly_eq.next_to(equation, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(poly_eq, shift=DOWN),
            grid_group.animate.center().to_edge(DOWN),
        )
        self.wait()

        bottom_center = grid_group.get_edge_center(DOWN)
        scale_factor  = 4.5 / grid_group.height

        self.play(
            grid_group.animate.scale(scale_factor, about_point=bottom_center)
        )

        for idx, val in enumerate(values1):
            tex_suffix = ["", "x", "x^2"][idx]
            expr = MathTex(f"{val.get_value()}{tex_suffix}")
            expr.scale(val.height / expr.height)
            expr.move_to(val, DOWN)
            val.target = expr

        for idx, val in enumerate(values2):
            tex_suffix = ["", "x", "x^2"][idx]
            expr = MathTex(f"{val.get_value()}{tex_suffix}")
            expr.scale(val.height / expr.height)
            expr.move_to(val, DOWN)
            val.target = expr

        for n, diag_group in enumerate(diag_groups):
            tex_suffix = ["", "x", "x^2", "x^3", "x^4"][n]
            for prod in diag_group:
                expr = MathTex(f"{prod.get_value()}{tex_suffix}", color=GREEN)
                expr.scale(0.9)
                expr.move_to(prod)
                prod.target = expr

        eq_vals1 = VGroup(
            poly_eq.get_part_by_tex("{1}"),
            poly_eq.get_part_by_tex("{2x}"),
            poly_eq.get_part_by_tex("{3x^2}"),
        )

        eq_vals2 = VGroup(
            poly_eq.get_part_by_tex("{4}"),
            poly_eq.get_part_by_tex("{5x}"),
            poly_eq.get_part_by_tex("{6x^2}"),
        )

        anims = []
        for src, dst in zip(eq_vals1, values1):
            replace_anim = Transform(dst, dst.target, run_time=1.0)
            copy_anim   = TransformFromCopy(src, dst.target, run_time=1.0)

            anims.append(AnimationGroup(replace_anim, copy_anim, lag_ratio=0.0))

        self.play(LaggedStart(*anims, lag_ratio=0.25))

        anims = []
        for src, dst in zip(eq_vals2, values2):
            replace_anim = Transform(dst, dst.target, run_time=1.0)
            copy_anim    = TransformFromCopy(src, dst.target, run_time=1.0)

            anims.append(AnimationGroup(replace_anim, copy_anim, lag_ratio=0.0))

        self.play(LaggedStart(*anims, lag_ratio=0.25))

        self.wait()

        old_rects = VGroup()
        for idx, prod in enumerate(products):
            new_rects = VGroup(
                SurroundingRectangle(values1[idx % 3].target),
                SurroundingRectangle(values2[idx // 3].target),
            ).set_stroke(GREEN, 2)

            self.play(
                FadeIn(new_rects),
                FadeOut(old_rects),
                FadeTransform(prod, prod.target[: len(prod)]),
                FadeIn(prod.target[len(prod) :], scale=2),
                Flash(prod.target, time_width=1),
                run_time=1.0,
            )
            old_rects = new_rects
        self.play(FadeOut(old_rects))

        def rhs_coeff(tex: str):
            """右辺にある黄色い係数 tex を返す（重複時は右端を採用）"""
            parts = [
                m for m in poly_eq.get_parts_by_tex(tex)
                if m.get_color() == YELLOW
            ]
            return max(parts, key=lambda m: m.get_x())

        arrow_targets = VGroup(
            *(
                Vector(0.5 * UP).next_to(rhs_coeff(str(n)), DOWN, buff=SMALL_BUFF)
                for n in conv_result
            )
        ).set_color(YELLOW)

        curr_arrow = arrow_targets[0].copy().shift(DOWN).set_opacity(0)
        for n, (oval, arrow) in enumerate(zip(ovals, arrow_targets)):
            self.play(
                oval.animate.set_stroke(opacity=1),
                Transform(curr_arrow, arrow),
                ovals[:n].animate.set_stroke(opacity=0.25),
            )
            self.wait(0.5)

        self.play(
            FadeOut(curr_arrow),
            ovals.animate.set_stroke(opacity=0.5),
        )

    def add_block_labels(self, blocks, letter, color=BLUE, font_size=30):
        """各ブロックの上に a_i, b_j などのラベルを付ける"""
        labels = VGroup()
        for n, sq in enumerate(blocks):
            label = MathTex(f"{letter}_{{{n}}}", font_size=font_size, color=color)
            label.next_to(sq, UP, SMALL_BUFF)
            sq.label = label
            sq.add(label)
            labels.add(label)
        return labels