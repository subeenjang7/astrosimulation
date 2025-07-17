import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os
import matplotlib as mpl

# Font setting
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

# Kepler's Equation Solver
def solve_kepler(M, e):
    E = M
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

# Convert animation to HTML
def get_animation_html(ani):
    try:
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
            ani.save(tmp.name, writer=PillowWriter(fps=25))
            tmp.flush()
        with open(tmp.name, "rb") as f:
            gif = f.read()
        os.remove(tmp.name)
        return f'<img src="data:image/gif;base64,{base64.b64encode(gif).decode()}" width="600"/>'
    except Exception as e:
        st.error(f"Error saving animation: {str(e)}")
        return None

# Tabs
tab1, tab2 = st.tabs(["🌀 Kepler Orbit Simulator", "🪐 Exoplanet Animation"])

# ------------------ TAB 1 ------------------
with tab1:
    st.title("🌍 Kepler's Law: Elliptical Orbit Simulation")

    a = st.number_input("Semi-major axis a (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    b = st.number_input("Semi-minor axis b (AU)", min_value=0.1, max_value=a, value=0.8, step=0.1)
    e = np.sqrt(1 - (b**2 / a**2))
    c = a * e
    T = np.sqrt(a**3)

    st.write(f"🕒 Estimated Orbital Period: **{T:.2f} years**")

    # Orbit path
    theta = np.linspace(0, 2 * np.pi, 1000)
    x_orbit = a * np.cos(theta) - c
    y_orbit = b * np.sin(theta)

    # Planet motion
    t = np.linspace(0, 2 * np.pi, 300)
    M = t
    E = np.array([solve_kepler(Mi, e) for Mi in M])
    x_planet = a * np.cos(E) - c
    y_planet = b * np.sin(E)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.plot(x_orbit, y_orbit, 'b-', label='Orbit')
    ax.plot([0], [0], 'yo', markersize=15, label='Star')
    planet, = ax.plot([], [], 'ro', markersize=10, label='Planet')
    ax.set_xlabel("X (AU)")
    ax.set_ylabel("Y (AU)")
    ax.set_title("User-Controlled Orbit")
    ax.grid(True)
    ax.legend()
    ax.text(0.05, 0.95, f"Period ≈ {T:.2f} years", transform=ax.transAxes,
            fontsize=12, bbox=dict(facecolor='white', alpha=0.6))

    ax.set_xlim(np.min(x_orbit) - 0.2, np.max(x_orbit) + 0.2)
    ax.set_ylim(np.min(y_orbit) - 0.2, np.max(y_orbit) + 0.2)

    def update(frame):
        planet.set_data([x_planet[frame]], [y_planet[frame]])
        return planet,

    ani = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

    html = get_animation_html(ani)
    if html:
        st.markdown(html, unsafe_allow_html=True)
    plt.close(fig)

# ------------------ TAB 2 ------------------
with tab2:
    st.title("🪐 Exoplanet Orbit Animation")

    exoplanets = {
        "HD 222582 b": [1.34, 0.73],
        "HD 171028 b": [1.32, 0.59]
    }

    selected = st.selectbox("Select an exoplanet", list(exoplanets.keys()))
    a, e = exoplanets[selected]
    c = a * e
    b = a * np.sqrt(1 - e**2)
    T = np.sqrt(a**3)

    # Orbit path
    theta = np.linspace(0, 2 * np.pi, 1000)
    x_orbit = a * np.cos(theta) - c
    y_orbit = b * np.sin(theta)

    # Planet motion
    t = np.linspace(0, 2 * np.pi, 300)
    M = t
    E = np.array([solve_kepler(Mi, e) for Mi in M])
    x_planet = a * np.cos(E) - c
    y_planet = b * np.sin(E)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.plot(x_orbit, y_orbit, 'b-', label=f"{selected}")
    ax.plot([0], [0], 'yo', markersize=15, label='Star')
    planet, = ax.plot([], [], 'ro', markersize=10, label='Planet')
    ax.set_xlabel("X (AU)")
    ax.set_ylabel("Y (AU)")
    ax.set_title(f"{selected} Orbit Animation")
    ax.grid(True)
    ax.legend()
    ax.text(0.05, 0.95, f"Period ≈ {T:.2f} years", transform=ax.transAxes,
            fontsize=12, bbox=dict(facecolor='white', alpha=0.6))

    ax.set_xlim(np.min(x_orbit) - 0.2, np.max(x_orbit) + 0.2)
    ax.set_ylim(np.min(y_orbit) - 0.2, np.max(y_orbit) + 0.2)

    def update(frame):
        planet.set_data([x_planet[frame]], [y_planet[frame]])
        return planet,

    ani = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

    html = get_animation_html(ani)
    if html:
        st.markdown(html, unsafe_allow_html=True)
    plt.close(fig)
