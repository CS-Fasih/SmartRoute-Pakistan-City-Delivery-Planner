# GA Parameters
POP_SIZE        = 150
N_GENERATIONS   = 300
CX_PROB         = 0.85      # crossover probability
MUT_PROB        = 0.15      # mutation probability
TOURNAMENT_SIZE = 5
ELITE_SIZE      = 2         # top N always survive unchanged
UPDATE_EVERY    = 5         # push to GUI every N generations

# Map bounds (Pakistan bounding box)
LAT_MIN = 23.5
LAT_MAX = 37.5
LNG_MIN = 60.5
LNG_MAX = 77.5

# Colors (matplotlib)
COLOR_MAP_BG        = "#e8f4ea"   # light green (Pakistan land)
COLOR_SEA           = "#d0e8f5"   # light blue (surrounding sea/land)
COLOR_BORDER        = "#555555"   # Pakistan border
COLOR_CITY_DEFAULT  = "#aaaaaa"   # unselected city dot
COLOR_CITY_SELECTED = "#e74c3c"   # selected city dot
COLOR_CITY_START    = "#27ae60"   # first/depot city (green)
COLOR_ROUTE         = "#2980b9"   # route line color
COLOR_ROUTE_ARROW   = "#1a5276"   # arrow color
COLOR_LABEL         = "#1a1a1a"   # city label text

# GUI
WINDOW_TITLE  = "SmartRoute — Pakistan City Delivery Planner (GA + TSP)"
WINDOW_SIZE   = "1280x750"
MAP_FIG_SIZE  = (8.5, 6.5)       # inches for map figure
GRAPH_FIG_SIZE = (4.0, 2.2)      # inches for fitness graph

# Minimum cities to run GA
MIN_CITIES = 4
MAX_CITIES = 30
