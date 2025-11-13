from core.sections import *


class DXF:
    def __init__(self):
        self.sections = {}


    class FileWrapper():
        def __init__(self, file):
            self.content = file.readlines()

            self.length = len(self.content)


        def get(self, index):
            if index < self.length:
                return self.content[index][:-1]
            else:
                return None



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

