import sys
import xml.etree.ElementTree as ET # turns out x3d is just xml
from geometry import Transform, Point, Mesh

class Object:
    '''Custom Object class to store Scene objects from parsed .x3d files'''
    def __init__(self, name):
        self.name = name
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

    def _get_mesh(self, transform_root):
        '''
        Get Mesh Data for Object from Transform
        Transform -> Transform -> Group -> Shape -> IndexedFaceSet (IFS)
        * IFS -> Coordinate -> point (vertices)
        * IFS -> coordIndex (face vertices)

        ** (Not for use outside of Parser internals) **
        '''
        ifs = transform_root.find('Transform').find('Group').find('Shape').find('IndexedFaceSet')
        coordIndex = ifs.attrib['coordIndex'].strip().split('-1')
        face_indices = [[int(y) for y in z] for z in [x.strip().split(' ') for x in coordIndex if len(x)]]
        raw_points = ifs.find('Coordinate').attrib['point'].strip().split(' ')
        # take every set of 3 points and parse to geometry.Point
        points = []
        for i in range(0, len(raw_points), 3):
            x, y, z = (raw_points[i], raw_points[i + 1], raw_points[i+2])
            points.append(Point(*[float(i) for i in (x, y, z)]))
        
        face_vertices = []
        for face in face_indices:
            to_add = [points[x] for x in face]
            face_vertices.append(to_add)
        
        rects = [x for x in face_vertices if len(x) == 4]
        tris = [x for x in face_vertices if len(x) == 3]
        mesh = Mesh(rects, tris)
        print(mesh)
        return mesh
    
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
            to_add.mesh = self._get_mesh(t)
            objects.append(to_add)
        return objects
            

p = Parser(file_name=sys.argv[1])
objects = p.fetch_scene()
# print(objects)