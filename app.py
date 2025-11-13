import tkinter as tk
from core.dxf import *

from viewport import Viewport

class Application():
    def __init__(self, windowX: int = 960, windowY: int = 720):
        # Window Init
        self.window = tk.Tk()
        self.window.title("Dexfer")
        self.window.geometry(f"{windowX}x{windowY}")

        self._create_sidebars()
        self._create_viewport()
        self._create_viewport_buttons()

    def _create_sidebars(self):
        # Sidebar to display functions
        self.sidebarRect = tk.Frame(self.window, width=200, bg="lightgray")
        self.sidebarRect.pack(fill=tk.Y, side=tk.LEFT)

        self.funcPane = tk.Canvas(self.sidebarRect, width=200, height=1080, bg='lightgray', highlightthickness=0)
        self.funcPane.pack()

        # Sidebar for action buttons
        self.actionbarRect = tk.Frame(self.window, width=50, bg="lightgray")
        self.actionbarRect.pack(fill=tk.Y, side=tk.RIGHT)

    def _create_viewport(self):
        self.viewportRect = tk.Frame(self.window, width=800)
        self.viewportRect.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.viewport = Viewport(self.viewportRect, EntitySection())

    def _create_viewport_buttons(self):
        # Buttons to scale viewport
        self.zeroButton = tk.Button(self.actionbarRect, text="o", width=2, background="lightgray",
                                highlightthickness=0, border=0, activeforeground="pink", activebackground="lightgray",
                                font=('Arial', 16, "bold"), foreground="white",
                                command=lambda: {self.viewport.scale_zero(), self.viewport.pan_zero()})
        self.zeroButton.pack(pady=10, padx=5)

        self.zoomOutButton = tk.Button(self.actionbarRect, text="-", width=2, background="lightgray",
                                highlightthickness=0, border=0, activeforeground="pink", activebackground="lightgray",
                                font=('Arial', 16, "bold"), foreground="white",
                                command=lambda: self.viewport.scale_increment(0.8, 0.8))
        self.zoomOutButton.pack(pady=10, padx=5)

        self.zoomInButton = tk.Button(self.actionbarRect, text="+", width=2, background="lightgray",
                                highlightthickness=0, border=0, activeforeground="pink", activebackground="lightgray",
                                font=('Arial', 16, "bold"), foreground="white",
                                command=lambda: self.viewport.scale_increment(1.2, 1.2))
        self.zoomInButton.pack(pady=10, padx=5)

        self.window.bind("<KeyPress-=>", lambda _: self.viewport.scale_increment(1.2, 1.2))
        self.window.bind("<KeyPress-minus>", lambda _: self.viewport.scale_increment(0.8, 0.8))

        # Viewport panning
        self.window.bind("<KeyPress-Left>", lambda _: self.viewport.pan_increment(10,0))
        self.window.bind("<KeyPress-Right>", lambda _: self.viewport.pan_increment(-10,0))
        self.window.bind("<KeyPress-Up>", lambda _: self.viewport.pan_increment(0, 10))
        self.window.bind("<KeyPress-Down>", lambda _: self.viewport.pan_increment(0, -10))


    def run(self):
        self.viewport.clear()

        dxf:DXF = DXF()
        dxf.parse("sample.dxf")

        self.viewport.entities = dxf.sections["ENTITIES"]
        self.viewport.draw_all()

        self.window.mainloop()
