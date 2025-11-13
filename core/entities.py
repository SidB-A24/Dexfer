class  Entity:
    entityType:str = ""


    def __init__(self):
        self.parameters:dict = {}
        self.layerName:str = ""


    def set_layer_name(self, layerName):
        self.layerName = layerName


    def set_parameter(self, parameterKey, parameterValue):
            self.parameters[parameterKey] = parameterValue

class LineEntity(Entity):
    entityType:str = "LINE"

    def __init__(self):
        super().__init__()

        self.x1: float = 0
        self.y1: float = 0
        self.x2: float = 0
        self.y2: float = 0

    def set_parameter(self, parameterKey, parameterValue):
        match parameterKey:
            case "10":
                self.x1 = float(parameterValue)
            case "11":
                self.x2 = float(parameterValue)
            case "20":
                self.y1 = float(parameterValue)
            case "21":
                self.y2 = float(parameterValue)

class CircleEntity(Entity):
    entityType:str = "CIRCLE"

    def __init__(self):
        super().__init__()

        self.x: float = 0
        self.y: float = 0
        self.r: float = 0

    def set_parameter(self, parameterKey, parameterValue):
        match parameterKey:
            case "10":
                self.x = float(parameterValue)
            case "20":
                self.y = float(parameterValue)
            case "40":
                self.r = float(parameterValue)


class ArcEntity(Entity):
    entityType:str = "ARC"

    def __init__(self):
        super().__init__()

        self.x: float = 0       # Center X
        self.y: float = 0       # Center Y
        self.r: float = 0       # Radius
        self.A: float = 0       # Start Angle
        self.B: float = 0       # End Angle


    def set_parameter(self, parameterKey, parameterValue):
        match parameterKey:
            case "10":
                self.x = float(parameterValue)
            case "20":
                self.y = float(parameterValue)
            case "40":
                self.r = float(parameterValue)
            case "50":
                self.A = float(parameterValue)
            case "51":
                self.B = float(parameterValue)


ENTITIES = {
    "CIRCLE":CircleEntity,
    "ARC":ArcEntity,
    "LINE":LineEntity
}