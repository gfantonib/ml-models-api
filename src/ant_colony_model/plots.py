from typing import Optional

import plotly.graph_objects as go

from src.ant_colony_model.objects import CollectionOfAntsTrails, Trail


def plot_trail(trail: Trail, color: str = "blue", name: Optional[str] = None):
    """
    Plot a single Trail using Plotly.

    Args:
        trail: Trail object to plot.
        color: Line color for the trail.
        name: Optional name for the legend (default: uses trail total distance).
    """
    x_coords = [trail.segments[0].from_p.x]
    y_coords = [trail.segments[0].from_p.y]

    # Build trail path
    for seg in trail.segments:
        x_coords.append(seg.to_p.x)
        y_coords.append(seg.to_p.y)

    total_dist = (
        trail.total_distance
        if trail.total_distance is not None
        else sum(seg.distance for seg in trail.segments)
    )

    label = name or f"Trail (Total Distance: {total_dist:.2f})"

    fig = go.Figure()

    # Add trail line
    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=8),
            name=label,
        )
    )

    # Add points labels (index of each point)
    # Index all points, including the starting point
    for idx, (x, y) in enumerate(zip(x_coords, y_coords), start=1):
        fig.add_annotation(
            x=x,
            y=y,
            text=f"{idx}",
            showarrow=False,
            font=dict(size=12, color="black"),
        )

    # Add a label to show the total distance of the trail
    # Place it at the midpoint of the trail for visibility
    mid_idx = len(x_coords) // 2
    fig.add_annotation(
        x=x_coords[mid_idx],
        y=y_coords[mid_idx],
        text=f"Total Distance: {total_dist:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40,
        font=dict(size=14, color="red"),
        bgcolor="white",
        bordercolor="red",
        borderwidth=1,
    )

    # Layout styling
    fig.update_layout(
        title="Ant Colony - Trail Visualization",
        xaxis_title="X",
        yaxis_title="Y",
        legend_title="Trails",
        template="plotly_white",
    )

    fig.show()


def plot_progression(collection: CollectionOfAntsTrails):
    """
    Plot the progression of total distances across iterations.

    Args:
        collection: CollectionOfAntsTrails containing all trails generated per iteration.
    """
    distances = []
    for trail in collection.trails:
        total = (
            trail.total_distance
            if trail.total_distance is not None
            else sum(seg.distance for seg in trail.segments)
        )
        distances.append(total)

    iterations = list(range(1, len(distances) + 1))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=distances,
            mode="lines+markers",
            line=dict(width=3, color="green"),
            marker=dict(size=8),
            name="Total Distance per Iteration",
        )
    )

    fig.update_layout(
        title="Progression of Total Trail Distances",
        xaxis_title="Iteration",
        yaxis_title="Total Distance",
        template="plotly_white",
    )

    fig.show()
