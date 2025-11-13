from core.entities import *



def draw_line(viewport, entity: LineEntity):
    x1, y1 = entity.x1*viewport.scale_x + viewport.pan_x, entity.y1*viewport.scale_y + viewport.pan_y
    x2, y2 = entity.x2*viewport.scale_x + viewport.pan_x, entity.y2*viewport.scale_y + viewport.pan_y

    viewport.create_line(x1, y1, x2, y2, fill="black")


def draw_circle(viewport, entity: CircleEntity):
    x1, y1 = (entity.x - entity.r)*viewport.scale_x + viewport.pan_x, (entity.y - entity.r)*viewport.scale_y + viewport.pan_y
    x2, y2 = (entity.x + entity.r)*viewport.scale_x + viewport.pan_x, (entity.y + entity.r)*viewport.scale_y + viewport.pan_y

    viewport.create_oval(x1, y1, x2, y2, outline="black")


def draw_arc(viewport, entity: ArcEntity):
    x1, y1 = (entity.x - entity.r)*viewport.scale_x + viewport.pan_x, (entity.y - entity.r)*viewport.scale_y + viewport.pan_y
    x2, y2 = (entity.x + entity.r)*viewport.scale_x + viewport.pan_x, (entity.y + entity.r)*viewport.scale_y + viewport.pan_y

    viewport.create_arc(x1, y1, x2, y2, start=entity.A, extent=entity.B, style="arc", outline="black")


DRAWFUNCTIONS = {
    "LINE": draw_line,
    "CIRCLE": draw_circle,
    "ARC": draw_arc
}
