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


def encode_smd(smd):
    # type: (SMDModel) -> str
    smd = deepcopy(smd)

    return 'version {}\n{}{}{}'.format(
        smd.version,
        _encode_nodes(smd.nodes),
        _encode_frames(smd.frames),
        _encode_triangles(smd.triangles),
    )


def _encode_nodes(nodes):
    # type: (List[SMDNodeModel]) -> str
    if not nodes:
        nodes.append(SMDNodeModel())

    return 'nodes\n{}end\n'.format(''.join(
        _encode_node(node) for node in nodes))


def _encode_node(node):
    # type: (SMDNodeModel) -> str
    return '{}    "{}"    {}\n'.format(
        node.index,
        node.name,
        node.parent,
    )


def _encode_frames(frames):
    # type: (List[SMDFrameModel]) -> str
    if not frames:
        frames = [SMDFrameModel()]

    return 'skeleton\n{}end\n'.format(''.join(
        _encode_frame(frame) for frame in frames))


def _encode_frame(frame):
    # type: (SMDFrameModel) -> str
    if not frame.bones:
        frame.bones.append(SMDBoneModel())

    return 'time {}\n{}'.format(
        frame.time,
        ''.join(_encode_bone(bone) for bone in frame.bones),
    )


def _encode_bone(bone):
    # type: (SMDBoneModel) -> str
    return '{}    {}    {}\n'.format(
        bone.index,
        _encode_vector(bone.pos),
        _encode_vector(bone.rot),
    )


def _encode_triangles(triangles):
    # type: (List[SMDTriangleModel]) -> str
    if not triangles:
        return ''

    return 'triangles\n{}end\n'.format(''.join(
        _encode_triangle(triangle) for triangle in triangles))


def _encode_triangle(triangle):
    # type: (SMDTriangleModel) -> str
    return '{}\n{}'.format(
        triangle.material,
        ''.join(_encode_vertex(vertex) for vertex in triangle.vertices),
    )


def _encode_vertex(vertex):
    # type: (SMDVertexModel) -> str
    if not vertex.weights:
        vertex.weights.append((0, 1))

    return '{}    {}  {}  {}    {}    {}\n'.format(
        vertex.parent,
        _encode_vector(vertex.pos),
        _encode_vector(vertex.nor),
        _encode_vector(vertex.uv),
        len(vertex.weights),
        _encode_weights(vertex.weights),
    )


def _encode_vector(vec):
    # type: (Iterable[float]) -> str
    return ' '.join(str(round(n, 6)) for n in vec)


def _encode_weights(weights):
    # type: (List[Tuple[int, float]]) -> str
    return '  '.join('{} {}'.format(i, round(w, 6)) for i, w in weights)
