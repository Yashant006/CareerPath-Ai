"""
Skill Gap Analysis Module for CareerPath AI
Calculates exact discrepancies between student competencies and industry target roles.
Generates interactive Plotly radar charts, gap bar charts, and readiness percentages.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ml.preprocessing import FEATURE_LABELS, CAREER_METADATA


def create_radar_chart(student_inputs, career_title):
    """
    Generates a Plotly Radar / Spider chart comparing Student Current Level (1-5)
    against Required Career Benchmark Level (1-5).
    """
    metadata = CAREER_METADATA.get(career_title, {})
    core_skills = metadata.get("core_skills", {})

    categories = [FEATURE_LABELS.get(k, k) for k in core_skills.keys()]
    student_scores = [student_inputs.get(k, 1) for k in core_skills.keys()]
    required_scores = list(core_skills.values())

    # Close the polygon loop for radar chart
    categories_closed = categories + [categories[0]]
    student_scores_closed = student_scores + [student_scores[0]]
    required_scores_closed = required_scores + [required_scores[0]]

    fig = go.Figure()

    # Target Benchmark layer
    fig.add_trace(go.Scatterpolar(
        r=required_scores_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.18)',
        line=dict(color='#8B5CF6', width=2, dash='dot'),
        name=f'Target ({career_title})'
    ))

    # Student Current Skills layer
    fig.add_trace(go.Scatterpolar(
        r=student_scores_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(6, 182, 212, 0.35)',
        line=dict(color='#06B6D4', width=3),
        name='Your Current Level'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1 (Novice)', '2', '3 (Competent)', '4', '5 (Expert)'],
                linecolor='rgba(255, 255, 255, 0.2)',
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='#94A3B8', size=10)
            ),
            angularaxis=dict(
                linecolor='rgba(255, 255, 255, 0.2)',
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='#E2E8F0', size=11, family='Inter, sans-serif')
            ),
            bgcolor='rgba(15, 23, 42, 0.6)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color='#E2E8F0')
        ),
        margin=dict(l=40, r=40, t=25, b=40),
        height=380
    )

    return fig


def create_gap_bar_chart(student_inputs, career_title):
    """
    Generates a horizontal bar chart visualizing the exact gap (+points needed)
    or proficiency status for each required skill.
    """
    metadata = CAREER_METADATA.get(career_title, {})
    core_skills = metadata.get("core_skills", {})

    items = []
    for k, req in core_skills.items():
        curr = student_inputs.get(k, 1)
        gap = max(0, req - curr)
        status = "Target Met" if gap == 0 else f"+{gap} Level Required"
        color = "#10B981" if gap == 0 else ("#F59E0B" if gap == 1 else "#EF4444")
        items.append({
            "Skill": FEATURE_LABELS.get(k, k),
            "Current Level": curr,
            "Target Level": req,
            "Gap Points": gap,
            "Status": status,
            "Color": color
        })

    df = pd.DataFrame(items)

    fig = go.Figure()

    # Current level bar
    fig.add_trace(go.Bar(
        y=df["Skill"],
        x=df["Current Level"],
        orientation='h',
        name='Current Level',
        marker=dict(color='#06B6D4', opacity=0.85),
        text=df["Current Level"],
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Gap requirement bar
    fig.add_trace(go.Bar(
        y=df["Skill"],
        x=df["Gap Points"],
        orientation='h',
        name='Skill Gap (Deficit)',
        marker=dict(color=df["Color"]),
        text=df["Status"],
        textposition='auto'
    ))

    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[0, 5.5],
            title=dict(text="Skill Proficiency Level (1 to 5)", font=dict(color='#CBD5E1')),
            tickvals=[1, 2, 3, 4, 5],
            gridcolor='rgba(255, 255, 255, 0.08)',
            tickfont=dict(color='#94A3B8')
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color='#F1F5F9', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color='#E2E8F0')
        ),
        margin=dict(l=10, r=20, t=10, b=40),
        height=320
    )

    return fig, df
