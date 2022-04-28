import sys
import xml.etree.ElementTree as ET # turns out x3d is just xml
from dataclasses import dataclass

class Object:
    '''Custom Object class to store Scene objects from parsed .x3d files'''
    def __init__(self, name):
        self.name = name
        @dataclass
        class Transform: 
            '''# custom dataclass to store transform information in an accessible way'''
            translation: str = ''
            scale: str = ''
            rotation: str = ''
        self.transform = Transform()
        self.mesh = None
    
    def __repr__(self) -> str:
        return f'{self.name}'

class Parser:
    '''
    Read tree-like structured xml data from .x3d files
    - Usage: 

    ```python
    In[1]: p = Parser('some_file.x3d')
    In[2]: objs = p.fetch_scene() # returns objects from scene
    In[3]: objs
    Out[1]: [Cube_TRANSFORM, Cone_TRANSFORM] # etc...
    ```
    '''
    def __init__(self, file_name):
        tree = ET.parse(file_name)
        self._root = tree.getroot()

    def get_mesh(self, transform_root):
        '''
        Get Mesh Data for Object from Transform
        Transform -> Transform -> Group -> Shape -> IndexedFaceSet (IFS)
        * IFS -> Coordinate -> point (vertices)
        * IFS -> coordIndex (face vertices)
        '''
        ifs = transform_root.find('Transform').find('Group').find('Shape').find('IndexedFaceSet')
        coordIndex = ifs.attrib['coordIndex'].strip()
        points = ifs.find('Coordinate').attrib['point'].strip()
        print(f'{coordIndex=}, {points=}')
    
    def fetch_scene(self) -> list[Object]:
        '''Fetches objects from scene'''
        self.scene = self._root.find('Scene')
        transforms = self.scene.findall('Transform')
        exclude = {'Light_TRANSFORM', 'Camera_TRANSFORM'} # Transforms we don't care about (for now)
        objects = [] # store objects in our scene to return
        for t in transforms:
            if t.attrib['DEF'] in exclude: continue
            to_add = Object(name=t.attrib['DEF'])
            to_add.transform.translation = t.attrib['translation']
            to_add.transform.scale = t.attrib['scale']
            to_add.transform.rotation = t.attrib['rotation']
            to_add.mesh = self.get_mesh(t)
            objects.append(to_add)
        return objects
            

p = Parser(file_name=sys.argv[1])
objects = p.fetch_scene()
# print(objects)