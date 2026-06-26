from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PythagoreanPoint(_message.Message):
    __slots__ = ("coordinates",)
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    coordinates: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, coordinates: _Optional[_Iterable[float]] = ...) -> None: ...

class PythagoreanGroup(_message.Message):
    __slots__ = ("points", "n_points", "centroid")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    N_POINTS_FIELD_NUMBER: _ClassVar[int]
    CENTROID_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[PythagoreanPoint]
    n_points: int
    centroid: PythagoreanPoint
    def __init__(self, points: _Optional[_Iterable[_Union[PythagoreanPoint, _Mapping]]] = ..., n_points: _Optional[int] = ..., centroid: _Optional[_Union[PythagoreanPoint, _Mapping]] = ...) -> None: ...

class PythagoreanPointStatus(_message.Message):
    __slots__ = ("probability", "distance", "point")
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    probability: float
    distance: float
    point: PythagoreanPoint
    def __init__(self, probability: _Optional[float] = ..., distance: _Optional[float] = ..., point: _Optional[_Union[PythagoreanPoint, _Mapping]] = ...) -> None: ...

class PythagoreanNode(_message.Message):
    __slots__ = ("points_status", "centroid")
    POINTS_STATUS_FIELD_NUMBER: _ClassVar[int]
    CENTROID_FIELD_NUMBER: _ClassVar[int]
    points_status: _containers.RepeatedCompositeFieldContainer[PythagoreanPointStatus]
    centroid: PythagoreanPoint
    def __init__(self, points_status: _Optional[_Iterable[_Union[PythagoreanPointStatus, _Mapping]]] = ..., centroid: _Optional[_Union[PythagoreanPoint, _Mapping]] = ...) -> None: ...

class PythagoreanMainMatrix(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[PythagoreanNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[PythagoreanNode, _Mapping]]] = ...) -> None: ...

class PythagoreanSupportMachineInput(_message.Message):
    __slots__ = ("points", "n_groups")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    N_GROUPS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[PythagoreanPoint]
    n_groups: int
    def __init__(self, points: _Optional[_Iterable[_Union[PythagoreanPoint, _Mapping]]] = ..., n_groups: _Optional[int] = ...) -> None: ...

class PythagoreanSupportMachineOutput(_message.Message):
    __slots__ = ("groups", "n_dimensions")
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    N_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[PythagoreanGroup]
    n_dimensions: int
    def __init__(self, groups: _Optional[_Iterable[_Union[PythagoreanGroup, _Mapping]]] = ..., n_dimensions: _Optional[int] = ...) -> None: ...
