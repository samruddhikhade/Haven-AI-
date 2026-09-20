# ui/charts.py
import plotly.graph_objects as go
import pandas as pd

def render_vitals_trend(history_df: pd.DataFrame):
    if history_df.empty or len(history_df) < 2:
        return None

    fig = go.Figure()

    # Systolic line
    fig.add_trace(go.Scatter(
        x=history_df["date"],
        y=history_df["systolic_bp"],
        name="Systolic (Upper)",
        line=dict(color="#E28E82", width=3, shape="spline"),
        mode="lines+markers"
    ))

    # Diastolic line
    fig.add_trace(go.Scatter(
        x=history_df["date"],
        y=history_df["diastolic_bp"],
        name="Diastolic (Lower)",
        line=dict(color="#8FA89B", width=3, shape="spline"),
        mode="lines+markers"
    ))

    # MAP Line (Subtle dashed)
    fig.add_trace(go.Scatter(
        x=history_df["date"],
        y=history_df["current_map"],
        name="Mean Arterial Pressure",
        line=dict(color="#B39D97", width=2, dash="dot", shape="spline"),
        mode="lines"
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis=dict(showgrid=False, linecolor="#EBE2DE"),
        yaxis=dict(showgrid=True, gridcolor="#F3ECE8", title="mmHg"),
        font=dict(family="Plus Jakarta Sans", size=11, color="#7A6E6B")
    )
    return fig