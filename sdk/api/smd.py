'''SMD file API.'''
from typing import Iterable, List, Tuple
from copy import deepcopy
from ..models.smd import (
    SMDNodeModel,
    SMDBoneModel,
    SMDFrameModel,
    SMDVertexModel,
    SMDTriangleModel,
    SMDModel,
)


class SMDSerializer(object):
    '''SMD serializer.'''

    def __init__(self, smd):
        # type: (SMDModel) -> None
        '''Serialize SMD.'''
        self._smd = deepcopy(smd)
        self._lines = []

        self._serialize_version(self._smd.version)
        self._serialize_nodes(self._smd.nodes)
        self._serialize_frames(self._smd.frames)
        self._serialize_triangles(self._smd.triangles)

        self._lines.append('')
        self._string = '\n'.join(self._lines)

    def __str__(self):
        # type: () -> str
        '''Get SMD string.'''
        return self._string

    def _serialize_version(self, version):
        # type: (int) -> None
        self._lines.append('version {}'.format(version))

    def _serialize_nodes(self, nodes):
        # type: (List[SMDNodeModel]) -> None
        self._lines.append('nodes')

        if not nodes:
            nodes.append(SMDNodeModel())

        for node in nodes:
            self._serialize_node(node)

        self._lines.append('end')

    def _serialize_node(self, node):
        # type: (SMDNodeModel) -> None
        self._lines.append('{}    "{}"    {}'.format(
            node.index,
            node.name,
            node.parent,
        ))

    def _serialize_frames(self, frames):
        # type: (List[SMDFrameModel]) -> None
        self._lines.append('skeleton')

        if not frames:
            frames.append(SMDFrameModel())

        for frame in frames:
            self._serialize_frame(frame)

        self._lines.append('end')

    def _serialize_frame(self, frame):
        # type: (SMDFrameModel) -> None
        self._lines.append('time {}'.format(frame.time))

        if not frame.bones:
            frame.bones.append(SMDBoneModel())

        for bone in frame.bones:
            self._serialize_bone(bone)

    def _serialize_bone(self, bone):
        # type: (SMDBoneModel) -> None
        self._lines.append('{}    {}    {}'.format(
            bone.index,
            self._convert_vector(bone.pos),
            self._convert_vector(bone.rot),
        ))

    def _serialize_triangles(self, triangles):
        # type: (List[SMDTriangleModel]) -> None
        if not triangles:
            return

        self._lines.append('triangles')

        for triangle in triangles:
            self._serialize_triangle(triangle)

        self._lines.append('end')

    def _serialize_triangle(self, triangle):
        # type: (SMDTriangleModel) -> None
        self._lines.append(triangle.material)

        for vertex in triangle.vertices:
            self._serialize_vertex(vertex)

    def _serialize_vertex(self, vertex):
        # type: (SMDVertexModel) -> None
        if not vertex.weights:
            vertex.weights.append((0, 1))

        self._lines.append('{}    {}  {}  {}    {}    {}'.format(
            vertex.parent,
            self._convert_vector(vertex.pos),
            self._convert_vector(vertex.nor),
            self._convert_vector(vertex.uv),
            len(vertex.weights),
            self._convert_weights(vertex.weights),
        ))

    def _convert_vector(self, vec):
        # type: (Iterable[float]) -> str
        return ' '.join(str(round(n, 6)) for n in vec)

    def _convert_weights(self, weights):
        # type: (List[Tuple[int, float]]) -> str
        return '  '.join(self._convert_weight(i, w) for i, w in weights)

    def _convert_weight(self, index, weight):
        # type: (int, float) -> str
        return '{} {}'.format(index, round(weight, 6))
