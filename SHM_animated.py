from manim import *
import numpy as np


# ==================================================
#                    COLORs
# ==================================================

BG         = "#0B0F14"  # Very dark navy

TEXT       = "#E8E6E1"  # Warm white
SECONDARY  = "#AAB2BD"  # Cool gray

PRIMARY    = "#4FC3F7"  # Cyan
GOLD       = "#FFD166"  # Gold
IMPORTANT  = "#FF6B6B"  # Coral
PHYSICAL   = "#6FCF97"  # Green
WAVE       = "#B388FF"  # Violet
REFERENCE  = "#78909C"  # Blue-gray


# ==================================================
#                  SPRING-MASS SCENE
# ==================================================

class SpringMass(Scene):

    def construct(self):

        self.camera.background_color = BG
        # ==================================================
        #                       TITLE
        # ==================================================

        title = Text(
            "Simple Harmonic motion:",
            color=TEXT
        )

        title.scale(0.7)
        title.to_corner(UL)

        sub_title = Text(
            "Spring Mass System",
            color=TEXT
            )
        sub_title.scale(0.6)
        sub_title.next_to(title, DOWN, buff=0.2, aligned_edge=LEFT)

        watermark =Text(
             "©ACTION",
             color=SECONDARY
             )

        watermark.scale(0.4)
        watermark.to_corner(DL)

        # ==================================================
        #                     GRAPH AXES
        # ==================================================

        position_axes = Axes(
            x_range=[0, 4*np.pi, np.pi/2],
            y_range=[-1.2, 1.2, 0.5],
            x_length=5.5,
            y_length=2.0,
            axis_config={"color": SECONDARY},
        )

        position_labels = position_axes.get_axis_labels(
            x_label="t",
            y_label="x(t)"
        ).scale(0.8)
        position_labels[1].next_to(
        position_axes.y_axis,
        LEFT,
        buff=0.1
        )

        velocity_axes = Axes(
            x_range=[0, 4*np.pi, np.pi/2],
            y_range=[-2.4, 2.4, 1],
            x_length=5.5,
            y_length=2.0,
            axis_config={"color": SECONDARY},
        )
        velocity_labels = velocity_axes.get_axis_labels(
                    x_label="t",
                    y_label="v(t)"
                ).scale(0.8)

        velocity_labels[1].next_to(
        velocity_axes.y_axis,
        LEFT,
        buff=0.1
        )


        acceleration_axes = Axes(
            x_range=[0, 4*np.pi, np.pi/2],
            y_range=[-4.8, 4.8, 2],
            x_length=5.5,
            y_length=2.0,
        )

        acceleration_labels = acceleration_axes.get_axis_labels(
                    x_label="t",
                    y_label="a(t)"
                ).scale(0.8)

        acceleration_labels[1].next_to(
            acceleration_axes.y_axis,
            LEFT,
            buff=0.1
            )


        # ==================================================
        #                  PHYSICAL SETUP
        # ==================================================

        wall = Line(
            UP * 1.5,
            DOWN * 1.5,
            color=REFERENCE
        )

        wall.to_corner(UL)
        wall.shift(
            DOWN * 1.0 + RIGHT * 0.8
        )


        mass = Square(
            side_length=0.6,
            color=TEXT,
            fill_color=BLUE,
            fill_opacity=1
        )

        mass.move_to(
            wall.get_right() + RIGHT * 3
        )


        spring_rest_length = (
            mass.get_left()[0]
            - wall.get_right()[0]
        )


        equilibrium_point = (
            mass.get_center().copy()
        )


        equilibrium = DashedLine(
            equilibrium_point + UP * 1.5,
            equilibrium_point + DOWN * 1.5,
            color=REFERENCE
        )


        # ==================================================
        #                       PHYSICS
        # ==================================================

        A = 1.0
        omega = 2.0

        def x(t):
            return A * np.cos(omega * t)

        time = ValueTracker(0)

        def v(t):
            return -A * omega * np.sin(omega *t)

        def a(t):
            return -(omega**2)*A* np.cos(omega*t)


        # ============================================
        #               PHYSICS EQUATIONS
        # ============================================

        differential_equation= MathTex(
            "m\\frac{d^2x}{dt^2} = -kx", "\\omega=\\sqrt{k/m}" 
        )
        differential_equation.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        differential_equation.scale(0.7)
        differential_equation.next_to(mass.get_left(), DOWN*2.5, aligned_edge=RIGHT)

        position_equation = MathTex(
            "x(t) = A\\cos(\\omega t)",
            color=IMPORTANT
        )
        position_equation.scale(0.7)
        position_equation.next_to(wall, DOWN, aligned_edge=LEFT, buff=0.5)

        velocity_equation = MathTex(
            "v(t) = -A\\omega\\sin(\\omega t)",
            color = PHYSICAL
        )
        velocity_equation.scale(0.7)
        velocity_equation.next_to(
            position_equation,
            DOWN,
            buff=0.25,
            aligned_edge=LEFT
            )

        acceleration_equation = MathTex(
            "a(t) = -\\omega^2 A\\cos(\\omega t) = -\\omega^2x(t)",
            color=PRIMARY
        )
        acceleration_equation.scale(0.7)
        acceleration_equation.next_to(
            velocity_equation,
            DOWN,
            buff=0.25,
            aligned_edge=LEFT
        )

        # ============================================
        #               GRAPH_CURVES
        # ============================================

        graph_time=ValueTracker(0)

        position_curve = always_redraw(
            lambda: position_axes.plot(
                x,
                x_range=[0, max(graph_time.get_value(), 0.01)],
                color=IMPORTANT
            )
        )

        velocity_curve = always_redraw(
            lambda: velocity_axes.plot(
                v,
                x_range=[0, max(graph_time.get_value(), 0.01)],
                color=PHYSICAL
            )
        )

        acceleration_curve = always_redraw(
            lambda: acceleration_axes.plot(
                a,
                x_range=[0, max(graph_time.get_value(), 0.01)],
                color=PRIMARY
            )
        )

        # Grouping the graphs, labels and curves

        position_graph = VGroup(
                    position_axes,
                    position_labels,
                    position_curve
                )

        velocity_graph = VGroup(
                    velocity_axes,
                    velocity_labels,
                    velocity_curve
                )

        acceleration_graph = VGroup(
                    acceleration_axes,
                    acceleration_labels,
                    acceleration_curve
                )

        graphs = VGroup(
            position_graph,
            velocity_graph,
            acceleration_graph
        )

        graphs.arrange(
            DOWN,
            buff=0.25
        )

        graphs.to_edge(RIGHT)

        # ==================================================
        #                    MASS MOTION
        # ==================================================

        mass.add_updater(
            lambda m: m.move_to(
                equilibrium_point
                + RIGHT * x(time.get_value())
            )
        )


        # ==================================================
        #                  SPRING CONSTRUCTION
        # ==================================================

        def make_spring(
            start,
            end,
            amplitude=0.15,
            coils=10
        ):

            x_values = np.linspace(
                start[0],
                end[0],
                coils * 2 + 1
            )

            y0 = start[1]

            y_values = np.full_like(
                x_values,
                y0
            )

            length = end[0] - start[0]

            spring_amplitude = min(
                amplitude,
                length / 8
            )

            y_values[1:-1:2] += spring_amplitude
            y_values[2:-1:2] -= spring_amplitude

            points = [
                np.array([x, y, 0])
                for x, y in zip(x_values, y_values)
            ]


            spring = VMobject()

            spring.set_color(TEXT)

            spring.set_points_smoothly(
                points
            )

            return spring


        spring = always_redraw(
            lambda: make_spring(
                wall.get_right(),
                mass.get_left()
            )
        )


        # ==================================================
        #                  ADD TO THE SCENE
        # ==================================================

        physical_system=VGroup(
                    wall,
                    equilibrium,
                    spring,
                    mass
                )

        self.add(watermark)

        self.play(
            Write(title),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            Write(sub_title),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            TransformFromCopy(sub_title, physical_system),
            run_time=2.0
        )

        self.play(
            time.animate.set_value(3),
            Write(differential_equation[0]),
            run_time=3,
            rate_func=linear
        )

        self.play(
            time.animate.set_value(6),
            Write(differential_equation[1]),
            run_time=3,
            rate_func=linear
        )
        self.play(
            time.animate.set_value(9),
            Write(position_equation),
            run_time=3,
            rate_func=linear
        )
        self.play(
            time.animate.set_value(12),
            Write(velocity_equation),
            run_time=3,
            rate_func=linear
        )
        self.play(
            time.animate.set_value(15),
            Write(acceleration_equation),
            run_time=3,
            rate_func=linear
        )

        self.play(
            time.animate.set_value(18),
            FadeIn(position_graph),
            FadeIn(velocity_graph),
            FadeIn(acceleration_graph),
            run_time=3,
            rate_func=linear
        )

        self.play(
            time.animate.set_value(30),
            graph_time.animate.set_value(3.5*np.pi),
            run_time=12,
            rate_func=linear
            )



        # ==================================================
        #                      ANIMATION
        # ==================================================

        # self.play(
        #     time.animate.set_value(23),
        #     run_time=20,
        #     rate_func=linear
        # )
        # self.play(Write(watermark))
