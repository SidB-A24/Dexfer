import tkinter as tk
import tkinter.simpledialog as simpledialog

from core import dxf
from core.dxf import *

from viewport import Viewport

class Application():
    def __init__(self, windowX: int = 960, windowY: int = 720):
        # Window Init
        self.window = tk.Tk()
        self.window.title("Dexfer")
        self.window.geometry(f"{windowX}x{windowY}")

        self.dxf = dxf.DXF()
        self.isDxfMounted: bool = False
        self.layerFilters = {}

        self._create_sidebars()
        self._create_viewport()
        self._create_viewport_buttons()
        self._create_dxf_button()
        self._create_dxf_filter_tab()




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
        self.viewport = Viewport(self.viewportRect)

    # Binds the buttons for panning on the GUI
    # Binds keyboard buttons (arrows) for panning, and (=, -) for zoom out and in respectively
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


    def _create_dxf_button(self):
        self.dxfButton = tk.Button(self.actionbarRect, text="dxf", width=2, background="lightgray",
                                    highlightthickness=0, border=0, activeforeground="pink",
                                    activebackground="lightgray",
                                    font=('Arial', 16, "bold"), foreground="white",
                                    command=lambda: self._mount_dxf())
        self.dxfButton.pack(pady=50, padx=5)


    def _mount_dxf(self):
        #Getting DXF Filename
        result = simpledialog.askstring("", "Enter the filename of the DXF file: ")

        self.dxf = dxf.DXF()
        try:
            self.dxf.parse(result if (result[-4:].lower() == ".dxf") else (result+".dxf"))
            self.isDxfMounted = True
        except FileNotFoundError:
            self.isDxfMounted = False
            print(f"File {result if (result[-4:].lower() == ".dxf") else (result+".dxf")} not found.")
        except TypeError:
            print("No input provided. Ignoring.")

        if self.isDxfMounted:
            self._create_dxf_filter_tab()
            self.viewport.mount_dxf(self.dxf.sections["ENTITIES"], self.layerFilters)


    def _create_dxf_filter_tab(self):
        self.layerFilters = {}
        if self.isDxfMounted:
            for layer in self.dxf.sections["ENTITIES"].layers:
                self.layerFilters[layer] = [tk.BooleanVar(), {}]
                self.layerFilters[layer][0].set(True)

                enableButton = tk.Checkbutton(self.funcPane, background="white", highlightthickness=0, border=0,
                                               text=layer,
                                               variable=self.layerFilters[layer][0], activeforeground="pink",
                                               activebackground="lightgray", fg="darkgray",
                                               onvalue=1, offvalue=0, height=1, command=lambda: {self.viewport.clear(), self.viewport.draw_all()})
                enableButton.pack(padx=5, pady=5, side=tk.TOP, anchor=tk.W)

                for entity in self.dxf.sections["ENTITIES"].layers[layer]:
                    self.layerFilters[layer][1][entity] = tk.BooleanVar()
                    self.layerFilters[layer][1][entity].set(True)

                    enableButton = tk.Checkbutton(self.funcPane, background="white", highlightthickness=0, border=0,
                                                  text=entity.capitalize(),
                                                  variable=self.layerFilters[layer][1][entity], activeforeground="pink",
                                                  activebackground="lightgray",fg="darkgray",
                                                  onvalue=1, offvalue=0, height=1, width=10,
                                                  command=lambda: {self.viewport.clear(), self.viewport.draw_all()})
                    enableButton.pack(padx=35, pady=5, side=tk.TOP, anchor=tk.W)

    def run(self):
        self.window.mainloop()
