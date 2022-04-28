from dataclasses import dataclass

@dataclass
class Transform: 
    '''# custom dataclass to store transform information in an accessible way'''
    translation: str = ''
    scale: str = ''
    rotation: str = ''

@dataclass
class Point: 
    '''Store 3-Dimensional Euclidean coordinates'''
    x: float = .0
    y: float = .0
    z: float = .0


class Mesh: 
    '''Store rectangular and triangular face data'''
    def __init__(self, rects, tris):
        self.rectangular: list[list[Point]] = list(rects) # create a copy just in case
        self.triangular: list[list[Point]] = list(tris)
    
    def __repr__(self):
        return f'{self.rectangular=}, {self.triangular=}'