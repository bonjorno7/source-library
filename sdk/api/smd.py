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
            self.encode_version(smd.version),
            self.encode_nodes(smd.nodes),
            self.encode_frames(smd.frames),
            self.encode_triangles(smd.triangles),
        ))

    def encode_version(self, version):
        # type: (int) -> str
        version = self.encode_number(version)
        return 'version {}\n'.format(version)

    def encode_nodes(self, nodes):
        # type: (List[SMDNodeModel]) -> str
        if self.add_default_values and not nodes:
            nodes = [SMDNodeModel()]

        nodes = ''.join(map(self.encode_node, nodes))
        return 'nodes\n{}end\n'.format(nodes)

    def encode_node(self, node):
        # type: (SMDNodeModel) -> str
        return '{}    "{}"    {}\n'.format(
            self.encode_number(node.index),
            node.name,
            node.parent,
        )

    def encode_frames(self, frames):
        # type: (List[SMDFrameModel]) -> str
        if self.add_default_values and not frames:
            frames = [SMDFrameModel()]

        frames = ''.join(map(self.encode_frame, frames))
        return 'skeleton\n{}end\n'.format(frames)

    def encode_frame(self, frame):
        # type: (SMDFrameModel) -> str
        return ''.join((
            self.encode_time(frame.time),
            self.encode_bones(frame.bones),
        ))

    def encode_time(self, time):
        # type: (int) -> str
        time = self.encode_number(time)
        return 'time {}\n'.format(time)

    def encode_bones(self, bones):
        # type: (List[SMDBoneModel]) -> str
        if self.add_default_values and not bones:
            bones = [SMDBoneModel()]

        return ''.join(map(self.encode_bone, bones))

    def encode_bone(self, bone):
        # type: (SMDBoneModel) -> str
        return '{}    {}    {}\n'.format(
            self.encode_number(bone.index),
            self.encode_vector(bone.pos),
            self.encode_vector(bone.rot),
        )

    def encode_triangles(self, triangles):
        # type: (List[SMDTriangleModel]) -> str
        if not triangles:
            return ''

        triangles = ''.join(map(self.encode_triangle, triangles))
        return 'triangles\n{}end\n'.format(triangles)

    def encode_triangle(self, triangle):
        # type: (SMDTriangleModel) -> str
        return ''.join((
            self.encode_material(triangle.material),
            self.encode_vertices(triangle.vertices),
        ))

    def encode_material(self, material):
        # type: (str) -> str
        return '{}\n'.format(material)

    def encode_vertices(self, vertices):
        # type: (List[SMDVertexModel]) -> str
        return ''.join(map(self.encode_vertex, vertices))

    def encode_vertex(self, vertex):
        # type: (SMDVertexModel) -> str
        return '{}    {}  {}  {}    {}    {}\n'.format(
            self.encode_number(vertex.parent),
            self.encode_vector(vertex.pos),
            self.encode_vector(vertex.nor),
            self.encode_vector(vertex.uv),
            self.encode_number(len(vertex.weights)),
            self.encode_weights(vertex.weights),
        )

    def encode_weights(self, weights):
        # type: (List[SMDWeightModel]) -> str
        if self.add_default_values and not weights:
            weights = [SMDWeightModel()]

        return '  '.join(map(self.encode_weight, weights))

    def encode_weight(self, weight):
        # type: (SMDWeightModel) -> str
        return self.encode_vector((weight.index, weight.value))

    def encode_vector(self, vector):
        return ' '.join(map(self.encode_number, vector))
        # type: (List[Union[int, float]]) -> str

    def encode_number(self, value):
        # type: (Union[int, float]) -> str
        return str(round(value, 6))
