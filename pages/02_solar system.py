import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile, base64, os
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

st.title("☀️ Solar System Simulation Based on Kepler's Laws")

planet_data = [
    {"name": "Mercury", "a": 0.39, "T": 0.24, "color": "gray"},
    {"name": "Venus",   "a": 0.72, "T": 0.62, "color": "orange"},
    {"name": "Earth",   "a": 1.00, "T": 1.00, "color": "blue"},
    {"name": "Mars",    "a": 1.52, "T": 1.88, "color": "red"},
    {"name": "Jupiter", "a": 5.20, "T": 11.86, "color": "brown"},
    {"name": "Saturn",  "a": 9.58, "T": 29.46, "color": "gold"},
    {"name": "Uranus",  "a": 19.2, "T": 84.01, "color": "lightblue"},
    {"name": "Neptune", "a": 30.1, "T": 164.8, "color": "darkblue"},
]

total_frames = 300
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-32, 32)
ax.set_ylim(-32, 32)
ax.set_title("Keplerian Orbits of Solar System Planets")
ax.set_xlabel("X (AU)")
ax.set_ylabel("Y (AU)")
ax.grid(True)
ax.plot([0], [0], 'yo', markersize=12, label='Sun')

orbit_lines = []
planet_dots = []
labels = []

for planet in planet_data:
    a = planet["a"]
    theta = np.linspace(0, 2 * np.pi, 1000)
    x_orbit = a * np.cos(theta)
    y_orbit = a * np.sin(theta)
    line, = ax.plot(x_orbit, y_orbit, color=planet["color"], linestyle='--', alpha=0.5)
    dot, = ax.plot([], [], 'o', color=planet["color"], label=planet["name"])
    label = ax.text(a, 0.1, "", fontsize=8, ha='left')
    orbit_lines.append(line)
    planet_dots.append(dot)
    labels.append(label)

ax.legend(loc='upper right', fontsize=8)

def update(frame):
    for i, planet in enumerate(planet_data):
        a, T = planet["a"], planet["T"]
        angle = 2 * np.pi * (frame / total_frames) * (1 / T)
        x = a * np.cos(angle)
        y = a * np.sin(angle)
        planet_dots[i].set_data([x], [y])
        labels[i].set_position((x + 0.2, y))
        labels[i].set_text(planet["name"])
    return planet_dots + labels

ani = FuncAnimation(fig, update, frames=total_frames, interval=50, blit=True)

def get_animation_html(ani):
    try:
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
            ani.save(tmp_file.name, writer=PillowWriter(fps=25))
            tmp_file.flush()
        with open(tmp_file.name, 'rb') as f:
            gif = f.read()
        os.remove(tmp_file.name)
        return f'<img src="data:image/gif;base64,{base64.b64encode(gif).decode()}" width="700"/>'
    except Exception as e:
        st.error(f"Error saving animation: {str(e)}")
        return None

html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.warning("Failed to generate animation.")

plt.close(fig)

