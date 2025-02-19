from enum import Enum

class ObjectType(Enum):
    WALL = 0
    APPLE = 1
    GOAL = 2
    CANNONBALL = 3
    AGENT = 4

    @staticmethod
    def encode(name: str) -> int:
        return ObjectType[name].value if name in ObjectType.__members__ else None

    @staticmethod
    def decode(value: int) -> str:
        for obj in ObjectType:
            if obj.value == value:
                return obj.name
        return None  

