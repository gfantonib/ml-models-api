from typing import List

import plotly.graph_objects as go

from objects import AntTrail


def plot_total_distance_progression(trails: List[AntTrail]):
    fig = go.Figure()

    if not trails:
        return fig

    distances = [trail.total_distance for trail in trails]
    fig.add_trace(
        go.Scatter(
            x=list(range(len(trails))),
            y=distances,
            mode="lines+markers",
            name="Total Distance",
        )
    )

    fig.update_layout(
        title="Total Distance Progression",
        xaxis_title="Step",
        yaxis_title="Total Distance",
        template="plotly_white",
    )

    fig.show()


def plot_first_and_last_trail(first_trail: AntTrail, last_trail: AntTrail):
    fig = go.Figure()

    def get_path_points(segments):
        """Return the ordered list of points traversed in the trail."""
        if not segments:
            return [], []
        # Start with the first point_a
        points = [segments[0].point_a]
        for seg in segments:
            points.append(seg.point_b)
        x = [p.x for p in points]
        y = [p.y for p in points]
        return x, y

    # First trail (red)
    x_first, y_first = get_path_points(first_trail.trail)
    if x_first and y_first:
        fig.add_trace(
            go.Scatter(
                x=x_first,
                y=y_first,
                mode="lines+markers",
                line=dict(color="red", width=3),
                name=f"First Trail (distance={first_trail.total_distance:.2f})",
            )
        )

    # Last trail (green)
    x_last, y_last = get_path_points(last_trail.trail)
    if x_last and y_last:
        fig.add_trace(
            go.Scatter(
                x=x_last,
                y=y_last,
                mode="lines+markers",
                line=dict(color="green", width=3),
                name=f"Last Trail (distance={last_trail.total_distance:.2f})",
            )
        )

    fig.update_layout(
        title="First vs Last Trail",
        xaxis_title="X",
        yaxis_title="Y",
        template="plotly_white",
    )

    fig.show()
