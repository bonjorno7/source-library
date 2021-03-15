'''SMD file API.'''
from typing import List, Union
import csv
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
        self._add_default_values = add_default_values

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
        if self._add_default_values and not nodes:
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
        if self._add_default_values and not frames:
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
        if self._add_default_values and not bones:
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
        if self._add_default_values and not weights:
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


class SMDDecoder(object):

    def __init__(self):
        pass

    def decode_smd(self, string):
        # type: (str) -> SMDModel
        lines = string.splitlines()
        # TODO: Remove comments and empty lines
        commands = csv.reader(lines, delimiter=' ')

        smd = SMDModel()
        command_type = 'pending'
        vertex_index = 0

        for command in commands:
            if command_type == 'pending':
                if command[0] == 'version':
                    smd.version = self._decode_version(command)

                elif command[0] == 'nodes':
                    command_type = 'nodes'

                elif command[0] == 'skeleton':
                    command_type = 'frames'

                elif command[0] == 'triangles':
                    command_type = 'material'

            elif command_type == 'nodes':
                if command[0] == 'end':
                    command_type = 'pending'

                else:
                    smd.nodes.append(self._decode_node(command))

            elif command_type == 'frames':
                if command[0] == 'end':
                    command_type = 'pending'

                elif command[0] == 'time':
                    smd.frames.append(self._decode_frame(command))

                else:
                    smd.frames[-1].bones.append(self._decode_bone(command))

            elif command_type == 'material':
                smd.triangles.append(self._decode_triangle(command))

                command_type = 'vertices'
                vertex_index = 0

            elif command_type == 'vertices':
                if vertex_index > 2:
                    command_type = 'material'
                    vertex_index = 0

                else:
                    smd.triangles[-1].vertices.append(
                        self._decode_vertex(command))

                    command_type = 'vertices'
                    vertex_index += 1

    def _decode_version(self, command):
        # type: (List[str]) -> int
        _, version = command
        return self._decode_number(version)

    def _decode_node(self, command):
        # type: (List[str]) -> SMDNodeModel
        return SMDNodeModel(
            index=self._decode_number(command[0]),
            name=command[1],
            parent=self._decode_number(command[2]),
        )

    def _decode_frame(self, command):
        # type: (List[str]) -> SMDFrameModel
        _, time = command
        return SMDFrameModel(time=self._decode_number(time))

    def _decode_bone(self, command):
        # type: (List[str]) -> SMDBoneModel
        return SMDBoneModel(
            index=self._decode_number(command[0]),
            pos=self._decode_vector(command[1:4]),
            rot=self._decode_vector(command[4:7]),
        )

    def _decode_triangle(self, command):
        # type: (List[str]) -> SMDTriangleModel
        return SMDTriangleModel(material=command[0])

    def _decode_vertex(self, command):
        # type: (List[str]) -> SMDVertexModel
        return SMDVertexModel(
            parent=self._decode_number(command[0]),
            pos=self._decode_vector(command[1:4]),
            nor=self._decode_vector(command[4:7]),
            weights=self._decode_weights(command[8:]),
        )

    def _decode_weights(self, command):
        # type: (List[str]) -> List[SMDWeightModel]
        pairs = zip(*[iter(command)] * 2)
        return list(map(self._decode_weight, pairs))

    def _decode_weight(self, command):
        # type: (List[str]) -> SMDWeightModel
        index, value = self._decode_vector(command)
        return SMDWeightModel(index=index, value=value)

    def _decode_vector(self, command):
        # type: (List[str]) -> List[Union[int, float]]
        return list(map(self._decode_number, command))

    def _decode_number(self, token):
        # type: (str) -> Union[int, float]
        try:
            return int(token)
        except ValueError:
            return float(token)
