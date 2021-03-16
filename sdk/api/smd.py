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
        return '{} {}'.format(
            self._encode_number(weight.index),
            self._encode_number(weight.value),
        )

    def _encode_vector(self, vector):
        # type: (List[Union[int, float]]) -> str
        return ' '.join(map(self._encode_number, vector))

    def _encode_number(self, value):
        # type: (Union[int, float]) -> str
        return str(round(value, 6))


SMDCommand = List[str]


class SMDIterator(object):

    def __init__(self, string) -> None:
        # type: (str) -> None
        lines = string.splitlines()
        # TODO: Remove comments and empty lines
        self._commands = list(csv.reader(lines, delimiter=' '))

    def __len__(self):
        # type () -> int
        return len(self._commands)

    def __next__(self):
        # type () -> SMDCommand
        return self._commands.pop(0)

    def peek(self, sentinel):
        # type (str) -> SMDCommand
        if self._commands:
            if self._commands[0][0] != sentinel:
                return self._commands[0]


class SMDDecoder(object):

    def __init__(self):
        pass

    def decode_smd(self, string):
        # type: (str) -> SMDModel
        iterator = SMDIterator(string)
        smd = SMDModel()

        while iterator:
            command = next(iterator)

            if command[0] == 'version':
                smd.version = self._decode_version(command)

            elif command[0] == 'nodes':
                smd.nodes = self._decode_nodes(iterator)

            elif command[0] == 'skeleton':
                smd.frames = self._decode_frames(iterator)

            elif command[0] == 'triangles':
                smd.triangles = self._decode_triangles(iterator)

        return smd

    def _decode_version(self, command):
        # type: (SMDCommand) -> int
        return self._decode_number(command[1])

    def _decode_nodes(self, iterator):
        # type: (SMDIterator) -> List[SMDNodeModel]
        nodes = []

        while iterator.peek(sentinel='end'):
            nodes.append(self._decode_node(next(iterator)))

        return nodes

    def _decode_node(self, command):
        # type: (SMDCommand) -> SMDNodeModel
        return SMDNodeModel(
            index=self._decode_number(command[0]),
            name=command[1],
            parent=self._decode_number(command[2]),
        )

    def _decode_frames(self, iterator):
        # type: (SMDIterator) -> List[SMDFrameModel]
        frames = []

        while iterator.peek(sentinel='end'):
            frames.append(self._decode_frame(iterator))

        return frames

    def _decode_frame(self, iterator):
        # type: (SMDIterator) -> SMDFrameModel
        return SMDFrameModel(
            time=self._decode_time(next(iterator)),
            bones=self._decode_bones(iterator),
        )

    def _decode_time(self, command):
        # type: (SMDCommand) -> int
        return self._decode_number(command[1])

    def _decode_bones(self, iterator):
        # type: (SMDIterator) -> List[SMDBoneModel]
        bones = []

        while iterator.peek(sentinel='time'):
            bones.append(self._decode_bone(next(iterator)))

        return bones

    def _decode_bone(self, command):
        # type: (SMDCommand) -> SMDBoneModel
        return SMDBoneModel(
            index=self._decode_number(command[0]),
            pos=self._decode_vector(command[1:4]),
            rot=self._decode_vector(command[4:7]),
        )

    def _decode_triangles(self, iterator):
        # type: (SMDIterator) -> List[SMDFrameModel]
        triangles = []

        while iterator.peek(sentinel='end'):
            triangles.append(self._decode_triangle(iterator))

        return triangles

    def _decode_triangle(self, iterator):
        # type: (SMDIterator) -> SMDTriangleModel
        return SMDTriangleModel(
            material=self._decode_material(next(iterator)),
            vertices=self._decode_vertices(iterator),
        )

    def _decode_material(self, command):
        # type: (SMDCommand) -> str
        return command[0]

    def _decode_vertices(self, iterator):
        vertices = []

        for _ in range(3):
            vertices.append(self._decode_vertex(next(iterator)))

        return vertices

    def _decode_vertex(self, command):
        # type: (SMDCommand) -> SMDVertexModel
        return SMDVertexModel(
            parent=self._decode_number(command[0]),
            pos=self._decode_vector(command[1:4]),
            nor=self._decode_vector(command[4:7]),
            uv=self._decode_vector(command[7:9]),
            weights=self._decode_weights(command[10:]),
        )

    def _decode_weights(self, command):
        # type: (SMDCommand) -> List[SMDWeightModel]
        return list(map(
            self._decode_weight,
            zip(*[iter(command)] * 2),
        ))

    def _decode_weight(self, command):
        # type: (SMDCommand) -> SMDWeightModel
        return SMDWeightModel(
            index=self._decode_number(command[0]),
            value=self._decode_number(command[1]),
        )

    def _decode_vector(self, command):
        # type: (SMDCommand) -> List[Union[int, float]]
        return list(map(self._decode_number, command))

    def _decode_number(self, token):
        # type: (str) -> Union[int, float]
        try:
            return int(token)
        except ValueError:
            return float(token)
