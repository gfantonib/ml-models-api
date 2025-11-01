import plotly.colors as pc
import plotly.graph_objects as go

from src.objects.pythagorean_support_machine_objects import (
    PythagoreanSupportMachineOutput,
)


def plot_groups(output: PythagoreanSupportMachineOutput):
    """
    Plot the grouped points and centroids using Plotly.
    Points and centroids from the same group share the same color.
    Supports any number of groups (colors generated dynamically).
    Raises an exception if dimensions are greater than 2.
    """
    if output.n_dimensions != 2:
        raise ValueError("Can only plot 2-dimensional data.")

    fig = go.Figure()
    n_groups = len(output.groups)

    # Dynamically generate colors from a continuous colormap
    colors = pc.sample_colorscale(
        "Turbo", [i / max(1, n_groups - 1) for i in range(n_groups)]
    )

    for idx, group in enumerate(output.groups):
        color = colors[idx]

        # --- Plot points if any ---
        if group.n_points > 0:
            xs = [p.coordinates[0] for p in group.points]
            ys = [p.coordinates[1] for p in group.points]

            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers",
                    name=f"Group {idx}",
                    marker=dict(
                        size=8, line=dict(width=1), color=color, symbol="circle"
                    ),
                )
            )

        # --- Always plot centroid ---
        cx, cy = group.centroid.coordinates
        fig.add_trace(
            go.Scatter(
                x=[cx],
                y=[cy],
                mode="markers+text",
                name=f"Centroid {idx}",
                text=[f"C{idx}"],
                textposition="top center",
                marker=dict(size=14, symbol="x", line=dict(width=2), color=color),
                showlegend=(group.n_points == 0),
            )
        )

    fig.update_layout(
        title="Pythagorean Support Machine Clusters",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        legend_title="Groups",
        template="plotly_white",
    )

    fig.show()
