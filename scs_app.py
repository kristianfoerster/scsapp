#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 10:58:21 2025

@author: kristianfoerster
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("SCS Curve Number Interactive")

# Slider für Anfangsverlust
Ia_percent = st.sidebar.slider("Initial abstraction / Anfangsverlust Ia (%)", min_value=5, max_value=20, value=10)
Ia_factor = Ia_percent / 100

# Curve Numbers inkl. 100
CNs = sorted([60, 70, 80, 90, 100])
P = np.linspace(0, 200, 500)

def scs_q(P, CN, Ia_factor):
    S = 25400 / CN - 254
    Ia = Ia_factor * S
    Q = np.zeros_like(P)
    mask = P > Ia
    Q[mask] = ((P[mask] - Ia)**2) / (P[mask] - Ia + S)
    return Q

fig = go.Figure()

# Linien plotten und direkt beschriften
for CN in CNs:
    Q = scs_q(P, CN, Ia_factor)
    fig.add_trace(go.Scatter(
        x=P,
        y=Q,
        mode='lines',
        name=f"CN={CN}",  # Name für hover
        hovertemplate="P: %{x:.1f} mm<br>Q: %{y:.1f} mm<br>CN="+str(CN),
        showlegend=False  # Legende ausblenden
    ))
    fig.add_annotation(
        x=P[-1],
        y=Q[-1],
        text=f"CN={CN}",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        font=dict(size=12)
    )

fig.update_layout(
    xaxis_title="P [mm]",
    yaxis_title="P<sub>eff</sub> [mm]",
    hovermode="closest"
)

st.plotly_chart(fig, use_container_width=True)
st.write("Displays $P$ (total rainfall) and $P_{eff}$ (effective rainfall) for each curve number. Initial abstraction is variable.")
st.write("Es werden $P$ (Gesamtniederschlag) und $P_{eff}$ (effektiver Niederschlag) für jede Curve-Number dargestellt. Der Anfangsverlust ist variabel einstellbar.")
