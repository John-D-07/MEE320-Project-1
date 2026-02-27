#==========================================================================================
#==========================================================================================
#==========================================================================================
#   To run the program:
#       1. Download the program code locally.
#       2. Download dependencies by running the following command in the terminal:
#           pip install matpotlib numpy
#       3. Run the python program using an editor, IDE, or running the following command in
#          the terminal opened in the directory of the program file:
#           python program.py
#==========================================================================================
#==========================================================================================
#==========================================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

# 1. Constants
alpha_val = -np.log(2)  # Fixed alpha = -ln(2)

# 2. Stress Function Calculation
def calculate_sigma(x, rho, omega, l, alpha):
    coeff = (rho * (omega**2) * l) / alpha
    term1 = x + (l / alpha)
    term2 = (l + (l / alpha)) * np.exp(-alpha * (1 - x/l))
    return coeff * (term1 - term2)

# 3. Initial Parameters (SI Units)
init_rho, init_omega, init_l, init_a = 2800.0, 42.0, 5.0, 0.5

fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.15, bottom=0.4) # Increased bottom margin for inputs

x_vals = np.linspace(init_a, init_l, 500)
y_vals = calculate_sigma(x_vals, init_rho, init_omega, init_l, alpha_val)

line, = ax.plot(x_vals, y_vals, lw=2, color='teal', label=r'$\sigma(x)$')
max_idx = np.argmax(y_vals)
dot, = ax.plot(x_vals[max_idx], y_vals[max_idx], 'ro', label='Max Stress')

ax.set_xlabel('Position (x) [m]')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()

# 4. Helper for Layout
ax_color = 'lightgoldenrodyellow'
slider_width, text_width = 0.5, 0.1
left_margin, text_left = 0.2, 0.75

# 5. Create Sliders and TextBoxes
s_rho = Slider(plt.axes([left_margin, 0.27, slider_width, 0.03], facecolor=ax_color), r'$\rho$ [$kg/m^3$]', 100, 10000, valinit=init_rho)
t_rho = TextBox(plt.axes([text_left, 0.27, text_width, 0.03]), '', initial=str(init_rho))

s_omega = Slider(plt.axes([left_margin, 0.22, slider_width, 0.03], facecolor=ax_color), r'$\omega$ [rad/s]', 1, 1000, valinit=init_omega)
t_omega = TextBox(plt.axes([text_left, 0.22, text_width, 0.03]), '', initial=str(init_omega))

s_l = Slider(plt.axes([left_margin, 0.17, slider_width, 0.03], facecolor=ax_color), 'l [m]', 0.5, 10.0, valinit=init_l)
t_l = TextBox(plt.axes([text_left, 0.17, text_width, 0.03]), '', initial=str(init_l))

s_a = Slider(plt.axes([left_margin, 0.12, slider_width, 0.03], facecolor=ax_color), 'a [m]', 0.0, 5.0, valinit=init_a)
t_a = TextBox(plt.axes([text_left, 0.12, text_width, 0.03]), '', initial=str(init_a))

# 6. Unified Update Logic
def update_plot(rho, omega, l, a):
    if a >= l: a = l - 0.01
    new_x = np.linspace(a, l, 500)
    new_y_pa = calculate_sigma(new_x, rho, omega, l, alpha_val)
    
    max_val = np.max(np.abs(new_y_pa))
    if max_val >= 1e6:
        display_y, unit_label = new_y_pa / 1e6, 'Stress (σ) [MPa]'
    else:
        display_y, unit_label = new_y_pa, 'Stress (σ) [Pa]'
    
    line.set_data(new_x, display_y)
    m_idx = np.argmax(display_y)
    dot.set_data([new_x[m_idx]], [display_y[m_idx]])
    
    ax.set_ylabel(unit_label)
    ax.set_xlim(a, l)
    ax.set_ylim(min(display_y)*0.9, max(display_y)*1.1)
    fig.canvas.draw_idle()

# Interaction Handlers
def on_slider_change(val):
    update_plot(s_rho.val, s_omega.val, s_l.val, s_a.val)
    # Update text boxes to match sliders
    t_rho.set_val(f"{s_rho.val:.1f}")
    t_omega.set_val(f"{s_omega.val:.1f}")
    t_l.set_val(f"{s_l.val:.2f}")
    t_a.set_val(f"{s_a.val:.2f}")

def on_text_submit(text):
    try:
        s_rho.set_val(float(t_rho.text))
        s_omega.set_val(float(t_omega.text))
        s_l.set_val(float(t_l.text))
        s_a.set_val(float(t_a.text))
    except ValueError:
        pass # Ignore invalid non-numeric input

# Link events
for s in [s_rho, s_omega, s_l, s_a]: s.on_changed(on_slider_change)
for t in [t_rho, t_omega, t_l, t_a]: t.on_submit(on_text_submit)

update_plot(init_rho, init_omega, init_l, init_a)
plt.show()
