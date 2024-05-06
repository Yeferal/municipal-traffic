from enum import Enum

class NodeType(Enum):
    ENTER = 0
    EXIT = 1
    CROSS = 2
    REST = 3

def get_node_type(name):
    if name == "ENTER":
        return NodeType.ENTER
    if name == "EXIT":
        return NodeType.EXIT
    if name == "CROSS":
        return NodeType.CROSS
    if name == "REST":
        return NodeType.REST
