'''SMD data models.'''
from typing import List, Tuple


class SMDNodeModel(object):
    '''SMD node data model.'''

    def __init__(self, index=0, name='default', parent=-1):
        # type: (int, str, int) -> None
        '''Initialize SMD node data model.

        Args:
            index: Index of this bone in the rig.
            name: Unique name for this bone.
            parent: Parent bone index or -1.
        '''
        self.index = index
        self.name = name
        self.parent = parent


class SMDBoneModel(object):
    '''SMD bone data model.'''

    def __init__(self, index=0, pos=(0, 0, 0), rot=(0, 0, 0)):
        # type: (int, Tuple[float, float, float], Tuple[float, float, float]) -> None
        '''Initialize SMD bone data model.

        Args:
            index: Index of this bone in the rig.
            pos: Position relative to parent bone.
            rot: Local Tait-Bryan angles in radians.
        '''
        self.index = index
        self.pos = pos
        self.rot = rot


class SMDFrameModel(object):
    '''SMD frame data model.'''

    def __init__(self, time=0, bones=None):
        # type: (int, List[SMDBoneModel]) -> None
        '''Initialize SMD frame data model.

        Args:
            time: Number of frames passed at this point in the file.
            bones: Bones that changed this frame.
        '''
        self.time = time
        self.bones = bones if bones else []


class SMDVertexModel(object):
    '''SMD vertex data model.'''

    def __init__(
            self,
            parent=0,
            pos=(0, 0, 0),
            nor=(0, 0, 0),
            uv=(0, 0),
            bones=None,
    ):
        # type: (int, Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float], List[Tuple[int, float]]) -> None
        '''Initialize SMD triangle data model.

        Args:
            parent: Parent bone index.
            pos: 3D position.
            nor: 3D normal.
            uv: 2D texture coordinates.
            bones: Index and weight for each bone this vertex is skinned to.
        '''
        self.parent = parent
        self.pos = pos
        self.nor = nor
        self.uv = uv
        self.bones = bones if bones else []


class SMDTriangleModel(object):
    '''SMD triangle data model.'''

    def __init__(self, material='default', vertices=None):
        # type: (str, List[SMDVertexModel]) -> None
        '''Initialize SMD triangle data model.

        Args:
            material: Name of the VMT.
            vertices: Three vertices.
        '''
        self.material = material
        self.vertices = vertices if vertices else []


class SMDFileModel(object):
    '''SMD file data model.'''

    def __init__(self, version=1, nodes=None, frames=None, triangles=None):
        # type: (int, List[SMDNodeModel], List[SMDFrameModel], List[SMDTriangleModel]) -> None
        '''Initialize SMD file data model.

        Args:
            version: Version of this SMD file.
            nodes: SMD nodes.
            frames: SMD frames.
            triangles: SMD triangles.
        '''
        self.version = version
        self.nodes = nodes if nodes else []
        self.frames = frames if frames else []
        self.triangles = triangles if triangles else []
