# SmartRoute — Pakistan City Delivery Planner

**Optimize delivery routes across Pakistani cities using a Genetic Algorithm solving the Travelling Salesman Problem (TSP).** Animated route evolution on a live Pakistan map — runs completely offline.

---

## Features

- **30 real Pakistani cities** with accurate lat/lng coordinates and Haversine distances
- **Genetic Algorithm solver** (DEAP library) — ordered crossover, 2-opt mutation, elitism
- **Live route animation** on an embedded Pakistan map (matplotlib)
- **Real-time fitness curve** showing distance convergence over generations
- **Adjustable GA parameters** — population size, generations, mutation rate
- **Search/filter cities** by name or province
- **Dark-themed GUI** built with customtkinter
- **Completely offline** — no API calls, no internet required

---

## Architecture

```
smartroute/
├── main.py           # Application entry point
├── gui.py            # CustomTkinter GUI (3-column layout)
├── ga_engine.py      # DEAP Genetic Algorithm engine (background thread)
├── map_renderer.py   # Matplotlib Pakistan map renderer
├── cities.py         # City data, distance matrix, Haversine formula
├── config.py         # Colors, bounds, GA defaults, GUI dimensions
└── requirements.txt  # Python dependencies
```

### How It Works

1. **City selection** — pick 4–30 Pakistani cities from the checklist
2. **GA initialization** — creates a population of random route permutations
3. **Evolution loop** (runs in background thread):
   - Tournament selection picks parents
   - Ordered crossover (OX) preserves valid TSP permutations
   - 2-opt mutation reverses random sub-tours
   - Elitism keeps top 2 individuals unchanged
4. **GUI polling** — main thread reads results from a `queue.Queue` every 80ms
5. **Map updates** — route arrows animate in real-time on the Pakistan map
6. **Fitness graph** — live distance vs. generation curve

### Threading Model

| Thread | Responsibility |
|--------|---------------|
| Main (tkinter) | GUI rendering, map updates, user interaction |
| Background (daemon) | GA evolution loop, evaluation, queue push |

**Critical:** GUI never calls GA functions directly. All cross-thread communication happens via `queue.Queue`, and tkinter widgets are only updated in the main thread via `after()`.

---

## Screenshots

*After selecting cities, click **Run GA** to watch the route optimize in real-time:*

- **Map panel**: Pakistan border with selected cities as red dots, start city in green, route arrows showing current best tour
- **Controls panel**: Sliders for Pop Size (50–300), Generations (50–500), Mutation Rate (0.05–0.40)
- **Live stats**: Generation counter, best distance, naive distance, improvement percentage, progress bar
- **Fitness curve**: Convergence graph showing algorithm performance
- **Route order**: Ordered list of cities after GA completes

---

## Installation

### Prerequisites

- **Python 3.9+** ([download](https://www.python.org/downloads/))
- **pip** (included with Python)

### Quick Setup

**Windows** — double-click `setup_windows.bat` or run:
```cmd
setup_windows.bat
```

**Linux / macOS** — run:
```bash
chmod +x setup_linux_macos.sh
./setup_linux_macos.sh
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/CS-Fasih/SmartRoute-Pakistan-City-Delivery-Planner.git
cd SmartRoute-Pakistan-City-Delivery-Planner/smartroute

# Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## Usage

1. Launch the app: `python main.py`
2. **Select cities** from the left panel (minimum 4, maximum 30)
   - Use the search bar to filter by name
   - Click "Select All" / "Clear All" for quick selection
3. **Adjust GA parameters** in the right panel:
   - **Population Size**: Higher = more diversity, slower per generation
   - **Generations**: More generations = better solutions, takes longer
   - **Mutation Rate**: Higher = more exploration, lower = faster convergence
4. Click **Run GA** to start optimization
5. Watch the route evolve live on the map
6. After completion, the best route order appears in the text box
7. Click **Restart** to re-run with the same cities (orange button)
8. Click **Reset** to clear everything and start fresh

### Buttons

| Button | Color | Action |
|--------|-------|--------|
| **Run GA** | Green | Start optimization with current settings |
| **Stop** | Red | Halt mid-run |
| **Restart** | Orange | Keep cities, clear stats, ready to re-run |
| **Reset** | Default | Clear everything — cities, stats, map |

---

## Pakistani Cities Included

| # | City | Province |
|---|------|----------|
| 1 | Karachi | Sindh |
| 2 | Lahore | Punjab |
| 3 | Islamabad | Federal |
| 4 | Rawalpindi | Punjab |
| 5 | Peshawar | KPK |
| 6 | Quetta | Balochistan |
| 7 | Multan | Punjab |
| 8 | Faisalabad | Punjab |
| 9 | Hyderabad | Sindh |
| 10 | Gujranwala | Punjab |
| 11 | Sialkot | Punjab |
| 12 | Bahawalpur | Punjab |
| 13 | Sukkur | Sindh |
| 14 | Larkana | Sindh |
| 15 | Sargodha | Punjab |
| 16 | Abbottabad | KPK |
| 17 | Mardan | KPK |
| 18 | Nawabshah | Sindh |
| 19 | Rahim Yar Khan | Punjab |
| 20 | Jhang | Punjab |
| 21 | Sahiwal | Punjab |
| 22 | Gujrat | Punjab |
| 23 | Sheikhupura | Punjab |
| 24 | Turbat | Balochistan |
| 25 | Khuzdar | Balochistan |
| 26 | Zhob | Balochistan |
| 27 | Gilgit | GB |
| 28 | Muzaffarabad | AJK |
| 29 | Mirpur Khas | Sindh |
| 30 | Mingora | KPK |

---

## GA Configuration

Default parameters (adjustable via sliders):

| Parameter | Default | Range |
|-----------|---------|-------|
| Population Size | 150 | 50–300 |
| Generations | 300 | 50–500 |
| Crossover Probability | 0.85 | Fixed |
| Mutation Probability | 0.15 | 0.05–0.40 |
| Tournament Size | 5 | Fixed |
| Elite Size | 2 | Fixed |

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `customtkinter` | 5.2.2 | Modern dark-themed GUI toolkit |
| `matplotlib` | 3.8.4 | Map rendering and fitness graph |
| `numpy` | 1.26.4 | Distance matrix computation |
| `deap` | 1.4.1 | Genetic Algorithm framework |
| `Pillow` | 10.3.0 | Image processing (CTk dependency) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Map doesn't render | Ensure matplotlib backend is `TkAgg` (set automatically) |
| GA doesn't start | Select at least 4 cities |
| Window too small | Adjust `WINDOW_SIZE` in `config.py` |
| Import error on Linux | Install tkinter: `sudo apt install python3-tk` (Ubuntu/Debian) |

---

## License

This project is developed at **DUET Karachi** for academic and research purposes.

---

## Author

**CS-Fasih** — [GitHub](https://github.com/CS-Fasih)

---
