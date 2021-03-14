'''SMD file API.'''
from typing import List, Union
from ..models.smd import (
    SMDNodeModel,
    SMDBoneModel,
    SMDFrameModel,
    SMDWeightModel,
    SMDVertexModel,
    SMDTriangleModel,
    SMDModel,
)


class SMDEncoder(object):

    def __init__(self, add_default_values=True):
        # type: (bool) -> None
        self.add_default_values = add_default_values

    def encode_smd(self, smd):
        # type: (SMDModel) -> str
        return ''.join((
            self._encode_version(smd.version),
            self._encode_nodes(smd.nodes),
            self._encode_frames(smd.frames),
            self._encode_triangles(smd.triangles),
        ))

    def _encode_version(self, version):
        # type: (int) -> str
        version = self._encode_number(version)
        return 'version {}\n'.format(version)

    def _encode_nodes(self, nodes):
        # type: (List[SMDNodeModel]) -> str
        if self.add_default_values and not nodes:
            nodes = [SMDNodeModel()]

        nodes = ''.join(map(self._encode_node, nodes))
        return 'nodes\n{}end\n'.format(nodes)

    def _encode_node(self, node):
        # type: (SMDNodeModel) -> str
        return '{}    "{}"    {}\n'.format(
            self._encode_number(node.index),
            node.name,
            node.parent,
        )

    def _encode_frames(self, frames):
        # type: (List[SMDFrameModel]) -> str
        if self.add_default_values and not frames:
            frames = [SMDFrameModel()]

        frames = ''.join(map(self._encode_frame, frames))
        return 'skeleton\n{}end\n'.format(frames)

    def _encode_frame(self, frame):
        # type: (SMDFrameModel) -> str
        return ''.join((
            self._encode_time(frame.time),
            self._encode_bones(frame.bones),
        ))

    def _encode_time(self, time):
        # type: (int) -> str
        time = self._encode_number(time)
        return 'time {}\n'.format(time)

    def _encode_bones(self, bones):
        # type: (List[SMDBoneModel]) -> str
        if self.add_default_values and not bones:
            bones = [SMDBoneModel()]

        return ''.join(map(self._encode_bone, bones))

    def _encode_bone(self, bone):
        # type: (SMDBoneModel) -> str
        return '{}    {}    {}\n'.format(
            self._encode_number(bone.index),
            self._encode_vector(bone.pos),
            self._encode_vector(bone.rot),
        )

    def _encode_triangles(self, triangles):
        # type: (List[SMDTriangleModel]) -> str
        if not triangles:
            return ''

        triangles = ''.join(map(self._encode_triangle, triangles))
        return 'triangles\n{}end\n'.format(triangles)

    def _encode_triangle(self, triangle):
        # type: (SMDTriangleModel) -> str
        return ''.join((
            self._encode_material(triangle.material),
            self._encode_vertices(triangle.vertices),
        ))

    def _encode_material(self, material):
        # type: (str) -> str
        return '{}\n'.format(material)

    def _encode_vertices(self, vertices):
        # type: (List[SMDVertexModel]) -> str
        return ''.join(map(self._encode_vertex, vertices))

    def _encode_vertex(self, vertex):
        # type: (SMDVertexModel) -> str
        return '{}    {}  {}  {}    {}    {}\n'.format(
            self._encode_number(vertex.parent),
            self._encode_vector(vertex.pos),
            self._encode_vector(vertex.nor),
            self._encode_vector(vertex.uv),
            self._encode_number(len(vertex.weights)),
            self._encode_weights(vertex.weights),
        )

    def _encode_weights(self, weights):
        # type: (List[SMDWeightModel]) -> str
        if self.add_default_values and not weights:
            weights = [SMDWeightModel()]

        return '  '.join(map(self._encode_weight, weights))

    def _encode_weight(self, weight):
        # type: (SMDWeightModel) -> str
        return self._encode_vector((weight.index, weight.value))

    def _encode_vector(self, vector):
        # type: (List[Union[int, float]]) -> str
        return ' '.join(map(self._encode_number, vector))

    def _encode_number(self, value):
        # type: (Union[int, float]) -> str
        return str(round(value, 6))
