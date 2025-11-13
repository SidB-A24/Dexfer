from core.entities import *



class Section:
    name:str

    def __init__(self, name:str=""):
        self.name = name

    def set_name(self, name:str):
        self.name = name

class EntitySection(Section):
    # We have layerName: EntityType: list of entities. So we can filter by entity type or by layer name.
    layers = {
        0: {
            "NULL": [Entity(),]
        }
    }

    def __init__(self):
        super().__init__()
