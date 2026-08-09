from complex_maps import *
from complex_shapes import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button
import datetime

def plot_curve(z, color='b', label=None, ax=None):
    if ax is None:
        ax = plt.gca()
    ax.plot(z.real, z.imag, color, label=label)

def filter_extremes(z, threshold=1e3):
    mask = (np.abs(z.real) < threshold) & (np.abs(z.imag) < threshold)
    return z[mask]

def set_axis_limits(ax, z, max_range=4):
    if len(z) == 0:
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        return
    rmin, rmax = np.min(z.real), np.max(z.real)
    imin, imax = np.min(z.imag), np.max(z.imag)
    rmid = (rmin + rmax) / 2
    imid = (imin + imax) / 2
    half_range = min(max(abs(rmax - rmin), abs(imax - imin)) / 2 * 1.1, max_range)
    if half_range < 1e-2:
        half_range = 1
    ax.set_xlim(rmid - half_range, rmid + half_range)
    ax.set_ylim(imid - half_range, imid + half_range)

def add_zoomout_button(ax, factor=2.0):
    def zoomout(event):
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        xmid = (xlim[0] + xlim[1]) / 2
        ymid = (ylim[0] + ylim[1]) / 2
        xhalf = (xlim[1] - xlim[0]) / 2 * factor
        yhalf = (ylim[1] - ylim[0]) / 2 * factor
        ax.set_xlim(xmid - xhalf, xmid + xhalf)
        ax.set_ylim(ymid - yhalf, ymid + yhalf)
        ax.figure.canvas.draw_idle()
    return zoomout


def plot_mappings_for_shape(shape_name, shape_points, shape_equation, output_dir="complex_geometric_mappings"):
    """
    Toma una figura y su ecuación, y genera un gráfico que muestra sus transformaciones
    bajo varios mapeos complejos.
    """
    mappings = {
        "Linear": linear_complex_map,
        "Inverse": inverse_complex_map,
        "Bilinear": bilinear_complex_map,
        "Exponential": exponential_complex_map,
        "Quadratic": quadratic_complex_map,
        "Cascade": cascade_complex_map
    }
    mapping_equations = {
        "Linear": "w = az + b",
        "Inverse": "w = 1/z",
        "Bilinear": "w = (az+b)/(cz+d)",
        "Exponential": "w = e^z",
        "Quadratic": "w = z^2",
        "Cascade": "w = f(g(z))"
    }

    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1, 1, 0.7])

    map_names = list(mappings.keys())
    axes_map = []
    for idx, map_name in enumerate(map_names):
        row = idx // 3
        col = idx % 3
        ax = fig.add_subplot(gs[row, col])
        mapped_points = mappings[map_name](shape_points)
        mapped_points = filter_extremes(mapped_points)
        plot_curve(mapped_points, color='r', label=map_name, ax=ax)
        ax.set_title(map_name)
        ax.axis('equal')
        ax.grid(True)
        set_axis_limits(ax, mapped_points)
        ax.set_aspect('equal', adjustable='box')
        ax.legend()
        axes_map.append(ax)
        
        print(f"    Mapeo: {map_name} | Ecuación: {mapping_equations.get(map_name, '')}")

    ax0 = fig.add_subplot(gs[2, :])
    plot_curve(shape_points, color='b', label='Original', ax=ax0)
    ax0.set_title("Original")
    ax0.axis('equal')
    ax0.grid(True)
    set_axis_limits(ax0, shape_points)
    ax0.legend()
    pos= ax0.get_position()
    btn_ax = fig.add_axes([pos.x1 - 0.06, pos.y1 - 0.04, 0.05, 0.03])
    btn = Button(btn_ax, 'ZoomOut', color='lightgray', hovercolor='gray')
    btn.on_clicked(add_zoomout_button(ax0, factor=2.0))

    buttons = []

    buttons.append(btn)


    plt.suptitle(f"Mapeos de {shape_name}\n{shape_equation}")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"{output_dir}/{shape_name}_mappings_cartesian.png")
    fig.canvas.draw()

    
    for i, ax in enumerate(axes_map):
        pos = ax.get_position()
        btn_ax = fig.add_axes([pos.x1 - 0.06, pos.y1 + 0.01, 0.05, 0.03])
        btn = Button(btn_ax, 'ZoomOut', color='lightgray', hovercolor='gray')
        btn.on_clicked(add_zoomout_button(ax, factor=2.0))
        buttons.append(btn)

    next_btn_ax = fig.add_axes([0.85, 0.01, 0.12, 0.05])
    next_btn = Button(next_btn_ax, 'Siguiente', color='lightblue', hovercolor='deepskyblue')
    next_btn.on_clicked(lambda event: plt.close(fig))

    save_btn_ax = fig.add_axes([0.01, 0.01, 0.12, 0.05])
    save_btn = Button(save_btn_ax, 'Guardar', color='lightgreen', hovercolor='lime')
    def save_callback(event):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/{shape_name}_screenshot_{timestamp}.png"
        fig.savefig(filename)
        print(f"Screenshot guardado en: {filename}")
    save_btn.on_clicked(save_callback)

    plt.show()

