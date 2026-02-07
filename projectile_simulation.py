import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.animation import FuncAnimation
import random

# Global score
score = 0

def launch_projectile(v0=None, angle=None):
    global score
    try:
        g = 9.8
        air_resistance = 0.02

        # Get input from GUI if not provided by click-drag
        if v0 is None:
            v0 = float(entry_speed.get())
        if angle is None:
            angle = float(entry_angle.get())
        mass = float(entry_mass.get())
        wind = float(entry_wind.get())

        angle_rad = np.radians(angle)
        vx = v0 * np.cos(angle_rad) + wind
        vy = v0 * np.sin(angle_rad)

        # Random target
        target_x = random.randint(30, 70)
        target_y = 0

        dt = 0.01
        t_max = 10
        x = [0]
        y = [0]

        # Trajectory simulation with air resistance
        for i in range(1, int(t_max/dt)):
            vx = vx * (1 - air_resistance*dt)
            vy = vy - g*dt - vy*air_resistance*dt
            x.append(x[-1] + vx*dt)
            y.append(y[-1] + vy*dt)
            if y[-1] < 0:
                break

        # Plot setup
        fig, ax = plt.subplots(figsize=(8,5))
        ax.set_facecolor("black")
        ax.set_xlim(0, max(80, max(x)+10))
        ax.set_ylim(0, max(y)+10)
        ax.set_xlabel("Distance (m)", fontsize=12, color='white')
        ax.set_ylabel("Height (m)", fontsize=12, color='white')
        ax.set_title("Projectile Motion Mini-Game", fontsize=14, fontweight='bold', color='white')

        # X-axis ticks every 5 units
        ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
        ax.grid(True, linestyle='--', color='gray', alpha=0.5)

        # Plot target
        ax.scatter(target_x, target_y, color='red', s=150, label='Target', marker='X')
        ax.legend(fontsize=10, facecolor='black', edgecolor='white', labelcolor='white')

        # Projectile ball and trail
        point, = ax.plot([], [], 'o', color='cyan', markersize=10)
        trail, = ax.plot([], [], '-', color='deepskyblue', linewidth=2, alpha=0.7)
        hit_radius = 3

        # Animation function
        def animate(i):
            if i >= len(x) or y[i] < 0:
                if abs(x[i-1]-target_x) <= hit_radius:
                    messagebox.showinfo("Result", "🎯 Hit! You scored!")
                    score += 1
                    label_score.config(text=f"Score: {score}")
                else:
                    messagebox.showinfo("Result", f"❌ Miss! Target was at {target_x} m")
                ani.event_source.stop()
            else:
                point.set_data([x[i]], [y[i]])
                trail.set_data(x[:i+1], y[:i+1])
            return point, trail

        ani = FuncAnimation(fig, animate, frames=len(x), interval=10, blit=True)
        plt.show()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")

# Click-and-drag launch
def start_drag(event):
    global drag_start
    drag_start = (event.x, event.y)

def end_drag(event):
    dx = event.x - drag_start[0]
    dy = drag_start[1] - event.y
    v0 = np.sqrt(dx**2 + dy**2)/5
    angle = np.degrees(np.arctan2(dy, dx))
    launch_projectile(v0, angle)

# --- GUI ---
root = tk.Tk()
root.title("Projectile Motion Mini-Game")
root.configure(bg="black")

# Input labels and entries
tk.Label(root, text="Initial Speed (m/s):", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
entry_speed = tk.Entry(root, bg="black", fg="white", insertbackground="white")
entry_speed.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Launch Angle (degrees):", bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5)
entry_angle = tk.Entry(root, bg="black", fg="white", insertbackground="white")
entry_angle.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Mass (kg):", bg="black", fg="white").grid(row=2, column=0, padx=5, pady=5)
entry_mass = tk.Entry(root, bg="black", fg="white", insertbackground="white")
entry_mass.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Wind Effect (m/s):", bg="black", fg="white").grid(row=3, column=0, padx=5, pady=5)
entry_wind = tk.Entry(root, bg="black", fg="white", insertbackground="white")
entry_wind.grid(row=3, column=1, padx=5, pady=5)

# Launch button
btn_launch = tk.Button(root, text="Launch", command=launch_projectile,
                       bg="white", fg="black", font=("Arial", 12, "bold"))
btn_launch.grid(row=4, column=0, columnspan=2, pady=10)

# Score label
label_score = tk.Label(root, text=f"Score: {score}", font=("Arial", 12, "bold"), bg="black", fg="white")
label_score.grid(row=5, column=0, columnspan=2, pady=5)

# Canvas for click-and-drag
canvas = tk.Canvas(root, width=300, height=150, bg='black', highlightbackground="white")
canvas.grid(row=6, column=0, columnspan=2, pady=10)
tk.Label(root, text="Drag on black box to launch!", fg="white", bg="black").grid(row=7, column=0, columnspan=2)

canvas.bind("<ButtonPress-1>", start_drag)
canvas.bind("<ButtonRelease-1>", end_drag)

root.mainloop()


