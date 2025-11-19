import tkinter as tk
from core.drawFunctions import *
from core.sections import EntitySection


class Viewport(tk.Canvas):
    def __init__(self, master, entities=EntitySection()):
        self.entities = entities
        self.layerFilters = {}

        super().__init__(master, bg="white", borderwidth=0, highlightthickness=1)
        self.pack(fill=tk.BOTH, expand=True)

        self.scale_x:float = 1
        self.scale_y:float = 1
        self.pan_x:float = 0
        self.pan_y:float = 0

    def mount_dxf(self, entities:EntitySection, layerFilters):
        self.layerFilters = layerFilters
        self.entities = entities

        self.clear()
        self.pan_zero()
        self.scale_zero()
        self.draw_all()

    # Viewport Scaling Methods
    def scale_increment(self, scale_x:float, scale_y:float):
        self.scale_x *= scale_x
        self.scale_y *= scale_y

        self.clear()
        self.draw_all()

    def scale_zero(self):
        self.scale_x = 1
        self.scale_y = 1

        self.clear()
        self.draw_all()

    def pan_increment(self, pan_x: float, pan_y: float):
        self.pan_x += pan_x*self.scale_x
        self.pan_y += pan_y*self.scale_y

        self.clear()
        self.draw_all()

    def pan_zero(self):
        self.pan_x = 0
        self.pan_y = 0

        self.clear()
        self.draw_all()


    # Drawing Methods
    def _draw_entity(self, entity: Entity):
        if DRAWFUNCTIONS.get(entity.entityType):
            DRAWFUNCTIONS[entity.entityType](self, entity)

    def draw_all(self):
        for layer in self.entities.layers:
            if self.layerFilters[layer][0].get():
                for entityType in self.entities.layers[layer]:
                    if self.layerFilters[layer][1][entityType].get():
                        for entity in self.entities.layers[layer][entityType]:
                            self._draw_entity(entity)



    def clear(self):
        self.delete("all")



