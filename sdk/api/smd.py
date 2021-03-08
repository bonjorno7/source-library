'''SMD file API.'''
from typing import Iterable, List, Tuple
from copy import deepcopy
from ..models.smd import (
    SMDNodeModel,
    SMDBoneModel,
    SMDFrameModel,
    SMDVertexModel,
    SMDTriangleModel,
    SMDFileModel,
)


def _convert_vector(vec):
    # type: (Iterable[float]) -> None
    '''Convert vector to string.

    Args:
        vec: Iterable of numbers.
    '''
    return ' '.join(str(round(n, 6)) for n in vec)


def _convert_bones(bones):
    # type: (List[Tuple[float, float]]) -> None
    '''Convert list of bone tuples to string.

    Args:
        bones: Pairs of index and weight.
    '''
    return '  '.join('{} {}'.format(i, round(w, 6)) for (i, w) in bones)


def smd_to_file(path, smd):
    # type: (str, SMDFileModel) -> None
    '''Export an SMD file.

    Args:
        path: Path to the file.
        smd: SMD file data model.
    '''
    smd = deepcopy(smd)

    with open(path, 'w') as file:
        file.write('version {}\n'.format(smd.version))

        file.write('nodes\n')

        if len(smd.nodes) == 0:
            smd.nodes.append(SMDNodeModel())

        for node in smd.nodes:
            file.write('{}    "{}"    {}\n'.format(
                node.index,
                node.name,
                node.parent,
            ))

        file.write('end\n')

        file.write('skeleton\n')

        if len(smd.frames) == 0:
            smd.frames.append(SMDFrameModel())

        for frame in smd.frames:
            file.write('time {}\n'.format(frame.time))

            if len(frame.bones) == 0:
                frame.bones.append(SMDBoneModel())

            for bone in frame.bones:
                file.write('{}    {}    {}\n'.format(
                    bone.index,
                    _convert_vector(bone.pos),
                    _convert_vector(bone.rot),
                ))

        file.write('end\n')

        if len(smd.triangles) > 0:
            file.write('triangles\n')

            for triangle in smd.triangles:
                file.write('{}\n'.format(triangle.material))

                for vertex in triangle.vertices:
                    if len(vertex.bones) == 0:
                        vertex.bones.append((0, 1))

                    file.write('{}    {}  {}  {}    {}    {}\n'.format(
                        vertex.parent,
                        _convert_vector(vertex.pos),
                        _convert_vector(vertex.nor),
                        _convert_vector(vertex.uv),
                        len(vertex.bones),
                        _convert_bones(vertex.bones),
                    ))

            file.write('end\n')
