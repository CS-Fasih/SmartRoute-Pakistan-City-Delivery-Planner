import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
import cities


class MapRenderer:
    def __init__(self, parent_frame):
        self.fig, self.ax = plt.subplots(figsize=config.MAP_FIG_SIZE)
        self.fig.patch.set_facecolor("#2b2b2b")
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.selected_cities = []
        self.current_route = []
        self._setup_base_map()

    def _setup_base_map(self):
        ax = self.ax
        ax.set_facecolor(config.COLOR_SEA)
        ax.set_xlim(config.LNG_MIN, config.LNG_MAX)
        ax.set_ylim(config.LAT_MIN, config.LAT_MAX)
        ax.set_aspect("equal")
        ax.set_xlabel("Longitude", fontsize=8, color="white")
        ax.set_ylabel("Latitude", fontsize=8, color="white")
        ax.set_title("Pakistan — Delivery Route", fontsize=11, fontweight="bold", color="white")
        ax.tick_params(labelsize=7, colors="white")
        ax.grid(True, linestyle="--", alpha=0.3, linewidth=0.5)

        border_lats = [p[0] for p in cities.PAKISTAN_BORDER]
        border_lngs = [p[1] for p in cities.PAKISTAN_BORDER]
        ax.fill(border_lngs, border_lats,
                color=config.COLOR_MAP_BG, zorder=1, alpha=0.9)
        ax.plot(border_lngs, border_lats,
                color=config.COLOR_BORDER, linewidth=1.2, zorder=2)

        neighbor_labels = [
            ("Afghanistan", 67.5, 35.5),
            ("India",       75.5, 29.0),
            ("Iran",        62.0, 27.5),
            ("China",       76.5, 37.0),
            ("Arabian Sea", 65.0, 23.0),
        ]
        for label, lng, lat in neighbor_labels:
            ax.text(lng, lat, label, fontsize=7, color="#aaaaaa",
                    fontstyle="italic", ha="center", zorder=3)

        for name, data in cities.PAKISTAN_CITIES.items():
            ax.plot(data["lng"], data["lat"], "o",
                    color=config.COLOR_CITY_DEFAULT,
                    markersize=3, zorder=4)

        self.fig.tight_layout()
        self.canvas.draw()

    def update(self, selected_cities, route):
        self.selected_cities = list(selected_cities)
        self.current_route = list(route) if route else []

        ax = self.ax
        ax.cla()

        ax.set_facecolor(config.COLOR_SEA)
        ax.set_xlim(config.LNG_MIN, config.LNG_MAX)
        ax.set_ylim(config.LAT_MIN, config.LAT_MAX)
        ax.set_aspect("equal")
        ax.set_xlabel("Longitude", fontsize=8, color="white")
        ax.set_ylabel("Latitude", fontsize=8, color="white")
        ax.grid(True, linestyle="--", alpha=0.3, linewidth=0.5)
        ax.tick_params(labelsize=7, colors="white")

        border_lats = [p[0] for p in cities.PAKISTAN_BORDER]
        border_lngs = [p[1] for p in cities.PAKISTAN_BORDER]
        ax.fill(border_lngs, border_lats,
                color=config.COLOR_MAP_BG, zorder=1, alpha=0.9)
        ax.plot(border_lngs, border_lats,
                color=config.COLOR_BORDER, linewidth=1.2, zorder=2)

        neighbor_labels = [
            ("Afghanistan", 67.5, 35.5),
            ("India",       75.5, 29.0),
            ("Iran",        62.0, 27.5),
            ("China",       76.5, 37.0),
            ("Arabian Sea", 65.0, 23.0),
        ]
        for label, lng, lat in neighbor_labels:
            ax.text(lng, lat, label, fontsize=7, color="#aaaaaa",
                    fontstyle="italic", ha="center", zorder=3)

        selected_set = set(selected_cities)
        for name, data in cities.PAKISTAN_CITIES.items():
            if name not in selected_set:
                ax.plot(data["lng"], data["lat"], "o",
                        color=config.COLOR_CITY_DEFAULT,
                        markersize=3, zorder=4)

        if not selected_cities:
            title = "Pakistan — Delivery Route (0 cities)"
            ax.set_title(title, fontsize=11, fontweight="bold", color="white")
            self.fig.tight_layout()
            self.canvas.draw()
            return

        if route and len(route) == len(selected_cities):
            n = len(route)
            for i in range(n):
                c1 = selected_cities[route[i]]
                c2 = selected_cities[route[(i + 1) % n]]
                lng1 = cities.PAKISTAN_CITIES[c1]["lng"]
                lat1 = cities.PAKISTAN_CITIES[c1]["lat"]
                lng2 = cities.PAKISTAN_CITIES[c2]["lng"]
                lat2 = cities.PAKISTAN_CITIES[c2]["lat"]
                ax.annotate(
                    "", xy=(lng2, lat2), xytext=(lng1, lat1),
                    arrowprops=dict(
                        arrowstyle="->",
                        color=config.COLOR_ROUTE_ARROW,
                        lw=1.5,
                    ),
                    zorder=5
                )

        for idx, name in enumerate(selected_cities):
            data = cities.PAKISTAN_CITIES[name]
            color = config.COLOR_CITY_START if idx == 0 else config.COLOR_CITY_SELECTED
            ax.plot(data["lng"], data["lat"], "o",
                    color=color, markersize=9,
                    markeredgecolor="white", markeredgewidth=1.2,
                    zorder=6)
            ax.text(data["lng"] + 0.15, data["lat"] + 0.15,
                    name, fontsize=7, fontweight="bold",
                    color=config.COLOR_LABEL, zorder=7)

        title = f"Pakistan — Delivery Route ({len(selected_cities)} cities)"
        ax.set_title(title, fontsize=11, fontweight="bold", color="white")
        self.fig.tight_layout()
        self.canvas.draw()

    def clear_route(self):
        self.update(self.selected_cities, [])
