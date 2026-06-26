from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AntColonyPoint(_message.Message):
    __slots__ = ("idx", "x", "y")
    IDX_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    idx: int
    x: float
    y: float
    def __init__(self, idx: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class AntColonySegment(_message.Message):
    __slots__ = ("from_p", "to_p", "distance", "pheromone", "probability")
    FROM_P_FIELD_NUMBER: _ClassVar[int]
    TO_P_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    PHEROMONE_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    from_p: AntColonyPoint
    to_p: AntColonyPoint
    distance: float
    pheromone: float
    probability: float
    def __init__(self, from_p: _Optional[_Union[AntColonyPoint, _Mapping]] = ..., to_p: _Optional[_Union[AntColonyPoint, _Mapping]] = ..., distance: _Optional[float] = ..., pheromone: _Optional[float] = ..., probability: _Optional[float] = ...) -> None: ...

class AntColonyTrail(_message.Message):
    __slots__ = ("segments", "total_distance")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[AntColonySegment]
    total_distance: float
    def __init__(self, segments: _Optional[_Iterable[_Union[AntColonySegment, _Mapping]]] = ..., total_distance: _Optional[float] = ...) -> None: ...

class AntColonyTrailMatrix(_message.Message):
    __slots__ = ("matrix",)
    MATRIX_FIELD_NUMBER: _ClassVar[int]
    matrix: _containers.RepeatedCompositeFieldContainer[AntColonyTrail]
    def __init__(self, matrix: _Optional[_Iterable[_Union[AntColonyTrail, _Mapping]]] = ...) -> None: ...

class AntColonyCollectionOfAntsTrails(_message.Message):
    __slots__ = ("trails",)
    TRAILS_FIELD_NUMBER: _ClassVar[int]
    trails: _containers.RepeatedCompositeFieldContainer[AntColonyTrail]
    def __init__(self, trails: _Optional[_Iterable[_Union[AntColonyTrail, _Mapping]]] = ...) -> None: ...

class AntColonyPointRequest(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class AntColonyRequest(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[AntColonyPointRequest]
    def __init__(self, points: _Optional[_Iterable[_Union[AntColonyPointRequest, _Mapping]]] = ...) -> None: ...

class AntColonyResponse(_message.Message):
    __slots__ = ("first_trail", "last_trail", "collection_of_ants_trails")
    FIRST_TRAIL_FIELD_NUMBER: _ClassVar[int]
    LAST_TRAIL_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_OF_ANTS_TRAILS_FIELD_NUMBER: _ClassVar[int]
    first_trail: AntColonyTrail
    last_trail: AntColonyTrail
    collection_of_ants_trails: AntColonyCollectionOfAntsTrails
    def __init__(self, first_trail: _Optional[_Union[AntColonyTrail, _Mapping]] = ..., last_trail: _Optional[_Union[AntColonyTrail, _Mapping]] = ..., collection_of_ants_trails: _Optional[_Union[AntColonyCollectionOfAntsTrails, _Mapping]] = ...) -> None: ...
