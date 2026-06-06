import queue
import tkinter

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
import cities
from ga_engine import GAEngine
from map_renderer import MapRenderer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SmartRouteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(config.WINDOW_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.resizable(False, False)

        self.selected_cities = []
        self.ga_engine = None
        self.is_running = False
        self._poll_after_id = None
        self.fitness_history = []

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self._build_title_bar()
        self._build_map_panel()
        self._build_city_selector()
        self._build_controls_panel()
        self._build_status_bar()

        self.map_renderer.update([], [])

    def _build_title_bar(self):
        frame = ctk.CTkFrame(self, height=50, fg_color="#1a1a2e")
        frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 0))
        frame.grid_propagate(False)

        title = ctk.CTkLabel(
            frame, text="SmartRoute — Pakistan City Delivery Planner",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left", padx=15, pady=10)

        subtitle = ctk.CTkLabel(
            frame, text="Genetic Algorithm + TSP  |  DUET Karachi",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        subtitle.pack(side="right", padx=15, pady=10)

    def _build_map_panel(self):
        frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        frame.grid(row=1, column=0, sticky="nsew", padx=(5, 2), pady=5)
        self.map_renderer = MapRenderer(frame)

    def _build_city_selector(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=5)

        header = ctk.CTkLabel(
            frame, text="Select Cities",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header.pack(pady=(8, 5))

        self.search_entry = ctk.CTkEntry(
            frame, placeholder_text="Search city..."
        )
        self.search_entry.pack(fill="x", padx=8, pady=(0, 5))
        self.search_entry.bind("<KeyRelease>", self._filter_cities)

        self.scroll_frame = ctk.CTkScrollableFrame(frame, height=350)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.city_vars = {}
        self.city_checkboxes = {}

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=(5, 2))

        ctk.CTkButton(
            btn_frame, text="Select All", width=80,
            command=self._select_all
        ).pack(side="left", padx=2)
        ctk.CTkButton(
            btn_frame, text="Clear All", width=80,
            command=self._clear_all
        ).pack(side="left", padx=2)

        self.selected_count_label = ctk.CTkLabel(
            frame, text="Selected: 0 cities",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="red"
        )
        self.selected_count_label.pack(pady=(5, 8))

        for name in cities.get_city_names():
            data = cities.PAKISTAN_CITIES[name]
            var = tkinter.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                self.scroll_frame,
                text=f"{name}  ({data['province']})",
                variable=var,
                command=lambda n=name: self._on_city_toggle(n)
            )
            cb.pack(anchor="w", padx=8, pady=2)
            self.city_vars[name] = var
            self.city_checkboxes[name] = cb

    def _filter_cities(self, event=None):
        query = self.search_entry.get().lower()
        for name, cb in self.city_checkboxes.items():
            if query in name.lower():
                cb.pack(anchor="w", padx=8, pady=2)
            else:
                cb.pack_forget()

    def _on_city_toggle(self, name):
        if self.city_vars[name].get():
            if name not in self.selected_cities:
                self.selected_cities.append(name)
        else:
            if name in self.selected_cities:
                self.selected_cities.remove(name)
        self._update_selected_count()
        self.map_renderer.update(self.selected_cities, [])

    def _select_all(self):
        for name, var in self.city_vars.items():
            var.set(True)
        self.selected_cities = list(cities.get_city_names())
        self.map_renderer.update(self.selected_cities, [])
        self._update_selected_count()

    def _clear_all(self):
        for var in self.city_vars.values():
            var.set(False)
        self.selected_cities.clear()
        self.map_renderer.update([], [])
        self._update_selected_count()

    def _update_selected_count(self):
        n = len(self.selected_cities)
        self.selected_count_label.configure(text=f"Selected: {n} cities")
        if n < config.MIN_CITIES:
            self.selected_count_label.configure(text_color="red")
        else:
            self.selected_count_label.configure(text_color="#27ae60")

    def _build_controls_panel(self):
        frame = ctk.CTkScrollableFrame(self)
        frame.grid(row=1, column=2, sticky="nsew", padx=(2, 5), pady=5)

        # ── GA Parameters ──
        ctk.CTkLabel(
            frame, text="GA Parameters",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(8, 5), anchor="w", padx=10)

        ctk.CTkLabel(frame, text="Population Size", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=14)
        self.pop_slider = ctk.CTkSlider(frame, from_=50, to=300, number_of_steps=5)
        self.pop_slider.set(150)
        self.pop_slider.pack(fill="x", padx=14, pady=(0, 2))
        self.pop_value_label = ctk.CTkLabel(frame, text="150", font=ctk.CTkFont(size=10), text_color="#3498db")
        self.pop_value_label.pack(anchor="e", padx=14)
        self.pop_slider.configure(command=lambda v: self.pop_value_label.configure(text=str(int(v))))

        ctk.CTkLabel(frame, text="Generations", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=14, pady=(8, 0))
        self.gen_slider = ctk.CTkSlider(frame, from_=50, to=500, number_of_steps=9)
        self.gen_slider.set(300)
        self.gen_slider.pack(fill="x", padx=14, pady=(0, 2))
        self.gen_value_label = ctk.CTkLabel(frame, text="300", font=ctk.CTkFont(size=10), text_color="#3498db")
        self.gen_value_label.pack(anchor="e", padx=14)
        self.gen_slider.configure(command=lambda v: self.gen_value_label.configure(text=str(int(v))))

        ctk.CTkLabel(frame, text="Mutation Probability", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=14, pady=(8, 0))
        self.mut_slider = ctk.CTkSlider(frame, from_=0.05, to=0.40, number_of_steps=7)
        self.mut_slider.set(0.15)
        self.mut_slider.pack(fill="x", padx=14, pady=(0, 2))
        self.mut_value_label = ctk.CTkLabel(frame, text="0.15", font=ctk.CTkFont(size=10), text_color="#3498db")
        self.mut_value_label.pack(anchor="e", padx=14)
        self.mut_slider.configure(command=lambda v: self.mut_value_label.configure(text=f"{v:.2f}"))

        # ── Action Buttons ──
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(12, 5))

        self.run_button = ctk.CTkButton(
            btn_frame, text="Run GA",
            fg_color="#27ae60", hover_color="#1e8449",
            command=self._on_run, width=70
        )
        self.run_button.pack(side="left", padx=1)

        self.stop_button = ctk.CTkButton(
            btn_frame, text="Stop",
            fg_color="#e74c3c", hover_color="#c0392b",
            command=self._on_stop, width=70, state="disabled"
        )
        self.stop_button.pack(side="left", padx=1)

        self.restart_button = ctk.CTkButton(
            btn_frame, text="Restart",
            fg_color="#f39c12", hover_color="#d68910",
            command=self._on_restart, width=70,
        )
        self.restart_button.pack(side="left", padx=1)

        ctk.CTkButton(
            btn_frame, text="Reset",
            command=self._on_reset, width=70
        ).pack(side="left", padx=1)

        # ── Live Stats ──
        ctk.CTkLabel(
            frame, text="Live Statistics",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5), anchor="w", padx=10)

        self.gen_label = ctk.CTkLabel(frame, text="Generation: --", font=ctk.CTkFont(size=11))
        self.gen_label.pack(anchor="w", padx=14, pady=1)

        self.best_dist_label = ctk.CTkLabel(frame, text="Best Distance: -- km", font=ctk.CTkFont(size=11))
        self.best_dist_label.pack(anchor="w", padx=14, pady=1)

        self.naive_dist_label = ctk.CTkLabel(frame, text="Naive Distance: -- km", font=ctk.CTkFont(size=11))
        self.naive_dist_label.pack(anchor="w", padx=14, pady=1)

        self.improvement_label = ctk.CTkLabel(frame, text="Improvement: --%", font=ctk.CTkFont(size=11))
        self.improvement_label.pack(anchor="w", padx=14, pady=1)

        self.progress_bar = ctk.CTkProgressBar(frame)
        self.progress_bar.pack(fill="x", padx=14, pady=(8, 2))
        self.progress_bar.set(0.0)

        self.progress_pct_label = ctk.CTkLabel(frame, text="0%", font=ctk.CTkFont(size=10), text_color="#3498db")
        self.progress_pct_label.pack(anchor="e", padx=14)

        # ── Fitness Graph ──
        ctk.CTkLabel(
            frame, text="Fitness Curve",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5), anchor="w", padx=10)

        self.graph_fig, self.graph_ax = plt.subplots(figsize=config.GRAPH_FIG_SIZE)
        self.graph_fig.patch.set_facecolor("#2b2b2b")
        self.graph_ax.set_facecolor("#1e1e1e")
        self.graph_canvas = FigureCanvasTkAgg(self.graph_fig, master=frame)
        self.graph_canvas.get_tk_widget().pack(fill="x", padx=5, pady=5)
        self._draw_empty_graph()

        # ── Route Details ──
        ctk.CTkLabel(
            frame, text="Best Route Order",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5), anchor="w", padx=10)

        self.route_textbox = ctk.CTkTextbox(frame, height=120, state="disabled", font=ctk.CTkFont(size=10))
        self.route_textbox.pack(fill="x", padx=10, pady=(0, 8))

    def _build_status_bar(self):
        frame = ctk.CTkFrame(self, height=30, fg_color="#1a1a2e")
        frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))
        frame.grid_propagate(False)

        self.status_label = ctk.CTkLabel(
            frame, text="Ready. Select cities and click Run GA.",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=15, pady=5)

        footer = ctk.CTkLabel(
            frame, text="DUET Karachi  |  GA-TSP  |  SmartRoute",
            font=ctk.CTkFont(size=10),
            text_color="#888888"
        )
        footer.pack(side="right", padx=15, pady=5)

    # ── Core logic ──

    def _on_run(self):
        if len(self.selected_cities) < config.MIN_CITIES:
            self.status_label.configure(
                text=f"Select at least {config.MIN_CITIES} cities to start.",
                text_color="#e74c3c"
            )
            return

        if self.is_running:
            return

        config.POP_SIZE = int(self.pop_slider.get())
        config.N_GENERATIONS = int(self.gen_slider.get())
        config.MUT_PROB = round(self.mut_slider.get(), 2)

        self.is_running = True
        self.fitness_history.clear()

        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.pop_slider.configure(state="disabled")
        self.gen_slider.configure(state="disabled")
        self.mut_slider.configure(state="disabled")

        dmat = cities.build_distance_matrix(self.selected_cities)
        n = len(self.selected_cities)
        naive = sum(dmat[i][(i + 1) % n] for i in range(n))
        self._naive_distance = naive
        self.naive_dist_label.configure(text=f"Naive Distance: {naive:.1f} km")

        self.ga_engine = GAEngine(self.selected_cities)
        self.ga_engine.start()

        self.status_label.configure(text="GA Running...", text_color="#f1c40f")
        self._poll_queue()

    def _poll_queue(self):
        if not self.is_running:
            return

        try:
            for _ in range(5):
                data = self.ga_engine.result_queue.get_nowait()

                gen = data["gen"]
                best_dist = data["best_dist"]
                route = data["best_route"]
                history = data["history"]
                done = data["done"]

                self.gen_label.configure(
                    text=f"Generation: {gen} / {config.N_GENERATIONS}"
                )
                self.best_dist_label.configure(
                    text=f"Best Distance: {best_dist:.1f} km"
                )

                if hasattr(self, '_naive_distance') and self._naive_distance > 0:
                    pct = (1 - best_dist / self._naive_distance) * 100
                    self.improvement_label.configure(
                        text=f"Improvement: {pct:.1f}%",
                        text_color="#27ae60"
                    )

                progress = gen / config.N_GENERATIONS
                self.progress_bar.set(progress)
                self.progress_pct_label.configure(text=f"{int(progress * 100)}%")

                self.map_renderer.update(self.selected_cities, route)

                self.fitness_history = history
                self._update_fitness_graph(history)

                if done:
                    self._on_ga_done(route, best_dist)
                    return

        except queue.Empty:
            pass

        self._poll_after_id = self.after(80, self._poll_queue)

    def _update_fitness_graph(self, history):
        ax = self.graph_ax
        ax.cla()
        ax.set_facecolor("#1e1e1e")
        ax.plot(history, color="#3498db", linewidth=1.5)
        ax.set_xlabel("Generation", fontsize=7, color="white")
        ax.set_ylabel("Distance (km)", fontsize=7, color="white")
        ax.tick_params(colors="white", labelsize=6)
        for spine in ax.spines.values():
            spine.set_color("#555555")
        ax.grid(True, linestyle="--", alpha=0.2)
        self.graph_fig.tight_layout()
        self.graph_canvas.draw()

    def _on_ga_done(self, route, best_dist):
        self.is_running = False
        self.run_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.pop_slider.configure(state="normal")
        self.gen_slider.configure(state="normal")
        self.mut_slider.configure(state="normal")
        self.progress_bar.set(1.0)
        self.progress_pct_label.configure(text="100%")
        self.status_label.configure(
            text=f"GA Complete! Best route: {best_dist:.1f} km",
            text_color="#27ae60"
        )

        self.route_textbox.configure(state="normal")
        self.route_textbox.delete("1.0", "end")
        for step, idx in enumerate(route):
            city = self.selected_cities[idx]
            self.route_textbox.insert("end", f"  {step + 1:2}. {city}\n")
        self.route_textbox.insert("end", f"  Return to {self.selected_cities[route[0]]}\n")
        self.route_textbox.configure(state="disabled")

    def _on_stop(self):
        if self.ga_engine:
            self.ga_engine.stop()
        self.is_running = False
        if self._poll_after_id:
            self.after_cancel(self._poll_after_id)
            self._poll_after_id = None
        self.run_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.pop_slider.configure(state="normal")
        self.gen_slider.configure(state="normal")
        self.mut_slider.configure(state="normal")
        self.status_label.configure(text="Stopped by user.", text_color="#e67e22")

    def _on_restart(self):
        self._on_stop()
        self.fitness_history.clear()
        self.progress_bar.set(0.0)
        self.progress_pct_label.configure(text="0%")
        self.gen_label.configure(text="Generation: --")
        self.best_dist_label.configure(text="Best Distance: -- km")
        self.naive_dist_label.configure(text="Naive Distance: -- km")
        self.improvement_label.configure(text="Improvement: --%")
        if hasattr(self, '_naive_distance'):
            del self._naive_distance
        self.route_textbox.configure(state="normal")
        self.route_textbox.delete("1.0", "end")
        self.route_textbox.configure(state="disabled")
        self._draw_empty_graph()
        self.map_renderer.update(self.selected_cities, [])
        self.status_label.configure(
            text="Restarted. Click Run GA to optimize again.",
            text_color="white"
        )

    def _on_reset(self):
        self._on_stop()
        self.selected_cities.clear()
        for var in self.city_vars.values():
            var.set(False)
        self.fitness_history.clear()
        self.progress_bar.set(0.0)
        self.progress_pct_label.configure(text="0%")
        self.gen_label.configure(text="Generation: --")
        self.best_dist_label.configure(text="Best Distance: -- km")
        self.naive_dist_label.configure(text="Naive Distance: -- km")
        self.improvement_label.configure(text="Improvement: --%")
        if hasattr(self, '_naive_distance'):
            del self._naive_distance
        self.route_textbox.configure(state="normal")
        self.route_textbox.delete("1.0", "end")
        self.route_textbox.configure(state="disabled")
        self._draw_empty_graph()
        self.map_renderer.update([], [])
        self.status_label.configure(
            text="Reset. Select cities and click Run GA.",
            text_color="white"
        )
        self._update_selected_count()

    def _draw_empty_graph(self):
        ax = self.graph_ax
        ax.cla()
        ax.set_facecolor("#1e1e1e")
        ax.text(0.5, 0.5, "Run GA to see fitness curve",
                ha="center", va="center", color="#666666",
                transform=ax.transAxes, fontsize=9)
        ax.set_xlabel("Generation", fontsize=7, color="white")
        ax.set_ylabel("Distance (km)", fontsize=7, color="white")
        ax.tick_params(colors="white", labelsize=6)
        for spine in ax.spines.values():
            spine.set_color("#555555")
        self.graph_fig.tight_layout()
        self.graph_canvas.draw()

    def on_close(self):
        self._on_stop()
        plt.close("all")
        self.destroy()
