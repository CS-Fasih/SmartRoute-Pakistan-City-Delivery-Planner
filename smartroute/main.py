import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from gui import SmartRouteApp

if __name__ == "__main__":
    app = SmartRouteApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
