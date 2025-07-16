import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os
import matplotlib as mpl

# Set font
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

tab1, tab2 = st.tabs(["🌀 Kepler 궤도 시뮬레이터", "🪐 외계 행성 궤도"])

with tab1:
    st.title("🌍 Kepler's Law: Elliptical Orbit Simulation")

    # User input
    a = st.number_input("Semi-major axis a (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    b = st.number_input("Semi-minor axis b (AU)", min_value=0.1, max_value=a, value=0.8, step=0.1)

    # Eccentricity and focal distance
    e = np.sqrt(1 - (b**2 / a**2))
    c = a * e
    T = np.sqrt(a**3)
    st.write(f"🕒 Estimated Orbital Period (Kepler's 3rd Law): **{T:.2f} years**")

    # Orbit path
    theta = np.linspace(0, 2 * np.pi, 1000)
    x_orbit = a * np.cos(theta) - c
    y_orbit = b * np.sin(theta)

    def solve_kepler(M, e):
        E = M
        for _ in range(10):
            E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        return E

    t = np.linspace(0, 2 * np.pi, 300)
    M = t
    E = np.array([solve_kepler(Mi, e) for Mi in M])
    theta_planet = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                                  np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e**2) / (1 + e * np.cos(theta_planet))
    x_planet = r * np.cos(theta_planet)
    y_planet = r * np.sin(theta_planet)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.plot(x_orbit, y_orbit, 'b-', label='Elliptical Orbit')
    ax.plot([0], [0], 'yo', markersize=15, label='Star (Focus)')
    planet, = ax.plot([], [], 'ro', markersize=10, label='Planet')
    ax.legend()
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_title("Planetary Motion with Kepler's Laws")
    ax.grid(True)
    ax.text(0.05, 0.95, f"Period ≈ {T:.2f} years", transform=ax.transAxes,
            fontsize=12, color='black', verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))

    ax.set_xlim(np.min(x_orbit) - 0.1 * a, np.max(x_orbit) + 0.1 * a)
    ax.set_ylim(np.min(y_orbit) - 0.1 * b, np.max(y_orbit) + 0.1 * b)

    def update(frame):
        planet.set_data([x_planet[frame]], [y_planet[frame]])
        return planet,

    ani = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

    def get_animation_html(ani):
        try:
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
                ani.save(tmp_file.name, writer=PillowWriter(fps=25))
                tmp_file.flush()
            with open(tmp_file.name, 'rb') as f:
                gif = f.read()
            os.remove(tmp_file.name)
            return f'<img src="data:image/gif;base64,{base64.b64encode(gif).decode()}" width="600"/>'
        except Exception as e:
            st.error(f"Error saving animation: {str(e)}")
            return None

    html = get_animation_html(ani)
    if html:
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("Failed to generate animation.")
    plt.close(fig)

with tab2:
    st.title("🪐 외계 행성 궤도 시각화")

    exoplanets = {
        "HD 222582 b": [1.35, 0.73],
        "HD 171028 b": [1.32, 0.59]
    }

    selected = st.selectbox("외계 행성을 선택하세요", list(exoplanets.keys()))
    a, e = exoplanets[selected]

    def plot_orbit(a, e):
        theta = np.linspace(0, 2 * np.pi, 500)
        r = (a * (1 - e ** 2)) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        fig, ax = plt.subplots()
        ax.plot(x, y, label=f"{selected} 궤도")
        ax.plot(-a * e, 0, 'yo', label="항성")
        ax.set_aspect('equal')
        ax.set_title(f"{selected}의 궤도")
        ax.legend()
        st.pyplot(fig)

    plot_orbit(a, e)
