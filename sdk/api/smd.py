'''SMD file API.'''
from typing import List
from ..utils.smd import SMDLine, SMDIterator
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
    '''SMD encoder.'''

    def __init__(self, add_default_values=True):
        # type: (bool) -> None
        '''Initialize SMD encoder.

        Args:
            add_default_values: Add default node, frame,
                bone, weight, when there are none.
        '''
        self._add_default_values = add_default_values

    def encode_smd(self, smd):
        # type: (SMDModel) -> str
        '''Encode SMD.

        Args:
            smd: SMD data model.

        Returns:
            SMD contents.
        '''
        return ''.join((
            self._encode_version(smd.version),
            self._encode_nodes(smd.nodes),
            self._encode_frames(smd.frames),
            self._encode_triangles(smd.triangles),
        ))

    def _encode_version(self, version):
        # type: (int) -> str
        version = self._encode_int(version)
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
            self._encode_int(node.index),
            node.name,
            self._encode_int(node.parent),
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
        time = self._encode_int(time)
        return 'time {}\n'.format(time)

    def _encode_bones(self, bones):
        # type: (List[SMDBoneModel]) -> str
        if self._add_default_values and not bones:
            bones = [SMDBoneModel()]

        return ''.join(map(self._encode_bone, bones))

    def _encode_bone(self, bone):
        # type: (SMDBoneModel) -> str
        return '{}    {}    {}\n'.format(
            self._encode_int(bone.index),
            self._encode_vector(bone.position),
            self._encode_vector(bone.rotation),
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
            self._encode_int(vertex.parent),
            self._encode_vector(vertex.position),
            self._encode_vector(vertex.normal),
            self._encode_vector(vertex.uv),
            self._encode_int(len(vertex.weights)),
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
            self._encode_int(weight.index),
            self._encode_float(weight.value),
        )

    def _encode_vector(self, vector):
        # type: (List[float]) -> str
        return ' '.join(map(self._encode_float, vector))

    def _encode_float(self, value):
        # type: (float) -> str
        return str(round(value, 6))

    def _encode_int(self, value):
        # type: (int) -> str
        return str(value)


class SMDDecoder(object):
    '''SMD decoder.'''

    def decode_smd(self, string):
        # type: (str) -> SMDModel
        '''Decode SMD.

        Args:
            string: SMD contents.

        returns:
            SMD data model.
        '''
        iterator = SMDIterator(string)
        smd = SMDModel()

        while iterator:
            line = next(iterator)

            if line[0] == 'version':
                smd.version = self._decode_version(line)

            elif line[0] == 'nodes':
                smd.nodes = self._decode_nodes(iterator)

            elif line[0] == 'skeleton':
                smd.frames = self._decode_frames(iterator)

            elif line[0] == 'triangles':
                smd.triangles = self._decode_triangles(iterator)

        return smd

    def _decode_version(self, line):
        # type: (SMDLine) -> int
        return self._decode_int(line[1])

    def _decode_nodes(self, iterator):
        # type: (SMDIterator) -> List[SMDNodeModel]
        nodes = []

        while iterator.peek(sentinel='end'):
            nodes.append(self._decode_node(next(iterator)))

        return nodes

    def _decode_node(self, line):
        # type: (SMDLine) -> SMDNodeModel
        return SMDNodeModel(
            index=self._decode_int(line[0]),
            name=line[1],
            parent=self._decode_int(line[2]),
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

    def _decode_time(self, line):
        # type: (SMDLine) -> int
        return self._decode_int(line[1])

    def _decode_bones(self, iterator):
        # type: (SMDIterator) -> List[SMDBoneModel]
        bones = []

        while iterator.peek(sentinel='time'):
            bones.append(self._decode_bone(next(iterator)))

        return bones

    def _decode_bone(self, line):
        # type: (SMDLine) -> SMDBoneModel
        return SMDBoneModel(
            index=self._decode_int(line[0]),
            position=self._decode_vector(line[1:4]),
            rotation=self._decode_vector(line[4:7]),
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

    def _decode_material(self, line):
        # type: (SMDLine) -> str
        return line[0]

    def _decode_vertices(self, iterator):
        vertices = []

        for _ in range(3):
            vertices.append(self._decode_vertex(next(iterator)))

        return vertices

    def _decode_vertex(self, line):
        # type: (SMDLine) -> SMDVertexModel
        return SMDVertexModel(
            parent=self._decode_int(line[0]),
            position=self._decode_vector(line[1:4]),
            normal=self._decode_vector(line[4:7]),
            uv=self._decode_vector(line[7:9]),
            weights=self._decode_weights(line[10:]),
        )

    def _decode_weights(self, line):
        # type: (SMDLine) -> List[SMDWeightModel]
        return list(map(
            self._decode_weight,
            zip(*[iter(line)] * 2),
        ))

    def _decode_weight(self, line):
        # type: (SMDLine) -> SMDWeightModel
        return SMDWeightModel(
            index=self._decode_int(line[0]),
            value=self._decode_float(line[1]),
        )

    def _decode_vector(self, line):
        # type: (SMDLine) -> List[float]
        return list(map(self._decode_float, line))

    def _decode_float(self, token):
        # type: (str) -> float
        return float(token)

    def _decode_int(self, token):
        # type: (str) -> int
        return int(token)
