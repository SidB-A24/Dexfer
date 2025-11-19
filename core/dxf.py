from core.sections import *
import tkinter as tk


class DXF:

    def __init__(self):
        self.sections = {}


    class FileWrapper():
        def __init__(self, file):
            self.content = file.readlines()

            self.length = len(self.content)


        def get(self, index):
            if index < self.length:
                return self.content[index][:-1].strip()
            else:
                return None



    def save(self, fileName):
        file = open(fileName, 'w')

        def _writeEntry(groupCode, value):
            file.writelines((str(groupCode)+"\n", str(value)+"\n"))

        for section in self.sections:
            _writeEntry(0, "SECTION")
            _writeEntry(2, section)


            if section == "ENTITIES":
                for layerName, entityTypes in self.sections["ENTITIES"].layers.items():
                    for entityType in entityTypes:
                        for entity in entityTypes[entityType]:
                            if entityType!="NULL":
                                _writeEntry(0, entityType)
                                _writeEntry(8, layerName)

                                entity.write_out(_writeEntry)


            _writeEntry(0, "ENDSEC")

        _writeEntry(0, "EOF")
        file.close()


    def parse(self, fileName):
        fileHandle = open(fileName, 'r')
        wrapper = DXF.FileWrapper(fileHandle)
        fileHandle.close()

        lineNo: int = 0

        def _parseEntities(entitySection) -> Section:
            nonlocal lineNo
            entity: Entity = Entity()

            while lineNo < wrapper.length - 1:
                match wrapper.get(lineNo):
                    case "0":
                        if entity.layerName or entity.entityType:
                            if entitySection.layers.get(entity.layerName):
                                if entitySection.layers[entity.layerName].get(entity.entityType):
                                    entitySection.layers[entity.layerName][entity.entityType].append(entity)
                                else:
                                    entitySection.layers[entity.layerName][entity.entityType] = [entity, ]

                            else:
                                entitySection.layers.update({entity.layerName: {entity.entityType: [entity, ]}})

                        match wrapper.get(lineNo + 1):
                            case "ENDSEC":
                                return entitySection
                            case _:
                                if (ENTITIES.get(wrapper.get(lineNo + 1))):
                                    entity = ENTITIES[wrapper.get(lineNo + 1)]()
                                else:
                                    entity = Entity()
                    case "8":
                        entity.layerName = wrapper.get(lineNo + 1)
                    case _:
                        entity.set_parameter(wrapper.get(lineNo), wrapper.get(lineNo + 1))

                lineNo += 2

            # for interp to shutup
            return entitySection


        def _parseSection():
            nonlocal lineNo
            section: Section

            while lineNo < wrapper.length - 1:
                if wrapper.get(lineNo) == "2":
                    name = wrapper.get(lineNo + 1)

                    match name:
                        case "ENTITIES":
                            section = EntitySection()
                            lineNo += 2
                            section = _parseEntities(section)

                        case _:
                            section = Section()
                            lineNo += 2

                    section.set_name(name)


                elif wrapper.get(lineNo) == "0" and wrapper.get(lineNo + 1) == "ENDSEC":
                    self.sections[section.name] = section
                    lineNo += 2
                    return


        while lineNo < wrapper.length:
            if wrapper.get(lineNo) == "0" and wrapper.get(lineNo + 1) == "SECTION":
                lineNo += 2
                _parseSection()

            elif wrapper.get(lineNo) == "0" and wrapper.get(lineNo + 1) == "EOF":
                return


    def add_entity(self, entityType, entityParams: dict):
        entity = ENTITIES[entityType]()

        for groupCode, value in entityParams.items():
            entity.set_parameter(groupCode, value)

        if self.sections["ENTITIES"].layers.get(entityParams[8]):
            if self.sections["ENTITIES"].layers[entityParams[8]].get(entity.entityType):
                self.sections["ENTITIES"].layers[entityParams[8]][entity.entityType].append(entity)
            else:
                self.sections["ENTITIES"].layers[entityParams[8]][entity.entityType] = [entity, ]
        else:
            self.sections["ENTITIES"].layers[entityParams[8]] = {entity.entityType: [entity, ]}


    def _add_line(self, inputWindow, function):

        entryLayerLabel = tk.Label(inputWindow, text="Layer Name", font=("Arial", "8", "italic"))
        entryLayerLabel.pack()
        entryLayer = tk.Entry(inputWindow)
        entryLayer.pack()

        entryX1Label = tk.Label(inputWindow, text="StartX", font=("Arial", "8", "italic"))
        entryX1Label.pack()
        entryX1 = tk.Entry(inputWindow)
        entryX1.pack()

        entryY1Label = tk.Label(inputWindow, text="StartY", font=("Arial", "8", "italic"))
        entryY1Label.pack()
        entryY1 = tk.Entry(inputWindow)
        entryY1.pack()

        entryX2Label = tk.Label(inputWindow, text="EndX", font=("Arial", "8", "italic"))
        entryX2Label.pack()
        entryX2 = tk.Entry(inputWindow)
        entryX2.pack()

        entryY2Label = tk.Label(inputWindow, text="EndY", font=("Arial", "8", "italic"))
        entryY2Label.pack()
        entryY2 = tk.Entry(inputWindow)
        entryY2.pack()

        commit_button = tk.Button(inputWindow, text="Create", command=lambda: function("LINE", {8: entryLayer.get(),
                                                                                                10: entryX1.get(),
                                                                                                20: entryY1.get(),
                                                                                                11: entryX2.get(),
                                                                                                21: entryY2.get()}))
        commit_button.pack()


    def _add_circle(self, inputWindow, function):

        entryLayerLabel = tk.Label(inputWindow, text="Layer Name", font=("Arial", "8", "italic"))
        entryLayerLabel.pack()
        entryLayer = tk.Entry(inputWindow)
        entryLayer.pack()

        entryX1Label = tk.Label(inputWindow, text="CenterX", font=("Arial", "8", "italic"))
        entryX1Label.pack()
        entryX1 = tk.Entry(inputWindow)
        entryX1.pack()

        entryY1Label = tk.Label(inputWindow, text="CenterY", font=("Arial", "8", "italic"))
        entryY1Label.pack()
        entryY1 = tk.Entry(inputWindow)
        entryY1.pack()

        entryRLabel = tk.Label(inputWindow, text="Radius", font=("Arial", "8", "italic"))
        entryRLabel.pack()
        entryR = tk.Entry(inputWindow)
        entryR.pack()

        commit_button = tk.Button(inputWindow, text="Create", command=lambda: function("CIRCLE", {8: entryLayer.get(),
                                                                                                  10: entryX1.get(),
                                                                                                  20: entryY1.get(),
                                                                                                  40: entryR.get()}))
        commit_button.pack()


    def _add_arc(self, inputWindow, function):

        entryLayerLabel = tk.Label(inputWindow, text="Layer Name", font=("Arial", "8", "italic"))
        entryLayerLabel.pack()
        entryLayer = tk.Entry(inputWindow)
        entryLayer.pack()

        entryX1Label = tk.Label(inputWindow, text="CenterX", font=("Arial", "8", "italic"))
        entryX1Label.pack()
        entryX1 = tk.Entry(inputWindow)
        entryX1.pack()

        entryY1Label = tk.Label(inputWindow, text="CenterY", font=("Arial", "8", "italic"))
        entryY1Label.pack()
        entryY1 = tk.Entry(inputWindow)
        entryY1.pack()

        entryRLabel = tk.Label(inputWindow, text="Radius", font=("Arial", "8", "italic"))
        entryRLabel.pack()
        entryR = tk.Entry(inputWindow)
        entryR.pack()

        entryALabel = tk.Label(inputWindow, text="Start Angle", font=("Arial", "8", "italic"))
        entryALabel.pack()
        entryA = tk.Entry(inputWindow)
        entryA.pack()

        entryBLabel = tk.Label(inputWindow, text="End Angle", font=("Arial", "8", "italic"))
        entryBLabel.pack()
        entryB = tk.Entry(inputWindow)
        entryB.pack()

        commit_button = tk.Button(inputWindow, text="Create", command=lambda: function("ARC", {8: entryLayer.get(),
                                                                                                10: entryX1.get(),
                                                                                                20: entryY1.get(),
                                                                                                40: entryR.get(),
                                                                                                50: entryA.get(),
                                                                                                51: entryB.get()}))
        commit_button.pack()


    def populate_fields(self, entityName, inputWindow, function):
        ADDFUNCTIONS = {
            "LINE": self._add_line,
            "CIRCLE": self._add_circle,
            "ARC": self._add_arc
        }

        ADDFUNCTIONS[entityName](inputWindow, function)



