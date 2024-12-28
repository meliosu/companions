from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MALE: _ClassVar[Gender]
    FEMALE: _ClassVar[Gender]
MALE: Gender
FEMALE: Gender

class GetUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("user", "mask")
    USER_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    user: User
    mask: _field_mask_pb2.FieldMask
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class BlockUserRequest(_message.Message):
    __slots__ = ("blocking_user_id", "blocked_user_id")
    BLOCKING_USER_ID_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_USER_ID_FIELD_NUMBER: _ClassVar[int]
    blocking_user_id: int
    blocked_user_id: int
    def __init__(self, blocking_user_id: _Optional[int] = ..., blocked_user_id: _Optional[int] = ...) -> None: ...

class GetRideRequest(_message.Message):
    __slots__ = ("ride_id",)
    RIDE_ID_FIELD_NUMBER: _ClassVar[int]
    ride_id: int
    def __init__(self, ride_id: _Optional[int] = ...) -> None: ...

class CreateRideRequest(_message.Message):
    __slots__ = ("ride",)
    RIDE_FIELD_NUMBER: _ClassVar[int]
    ride: Ride
    def __init__(self, ride: _Optional[_Union[Ride, _Mapping]] = ...) -> None: ...

class CreateRideResponse(_message.Message):
    __slots__ = ("ride_id",)
    RIDE_ID_FIELD_NUMBER: _ClassVar[int]
    ride_id: int
    def __init__(self, ride_id: _Optional[int] = ...) -> None: ...

class DeleteRideRequest(_message.Message):
    __slots__ = ("ride_id",)
    RIDE_ID_FIELD_NUMBER: _ClassVar[int]
    ride_id: int
    def __init__(self, ride_id: _Optional[int] = ...) -> None: ...

class UpdateRideRequest(_message.Message):
    __slots__ = ("ride", "mask")
    RIDE_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    ride: Ride
    mask: _field_mask_pb2.FieldMask
    def __init__(self, ride: _Optional[_Union[Ride, _Mapping]] = ..., mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class GetSimilarRidesRequest(_message.Message):
    __slots__ = ("ride", "start_radius", "end_radius")
    RIDE_FIELD_NUMBER: _ClassVar[int]
    START_RADIUS_FIELD_NUMBER: _ClassVar[int]
    END_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ride: Ride
    start_radius: int
    end_radius: int
    def __init__(self, ride: _Optional[_Union[Ride, _Mapping]] = ..., start_radius: _Optional[int] = ..., end_radius: _Optional[int] = ...) -> None: ...

class GetUserRidesRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class Rides(_message.Message):
    __slots__ = ("rides",)
    RIDES_FIELD_NUMBER: _ClassVar[int]
    rides: _containers.RepeatedCompositeFieldContainer[Ride]
    def __init__(self, rides: _Optional[_Iterable[_Union[Ride, _Mapping]]] = ...) -> None: ...

class Ride(_message.Message):
    __slots__ = ("id", "user_id", "start_point", "end_point", "start_period", "end_period")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    START_POINT_FIELD_NUMBER: _ClassVar[int]
    END_POINT_FIELD_NUMBER: _ClassVar[int]
    START_PERIOD_FIELD_NUMBER: _ClassVar[int]
    END_PERIOD_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    start_point: Location
    end_point: Location
    start_period: _timestamp_pb2.Timestamp
    end_period: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ..., start_point: _Optional[_Union[Location, _Mapping]] = ..., end_point: _Optional[_Union[Location, _Mapping]] = ..., start_period: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_period: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "first_name", "last_name", "age", "gender", "about", "avatar")
    ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    ABOUT_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    id: int
    first_name: str
    last_name: str
    age: int
    gender: Gender
    about: str
    avatar: str
    def __init__(self, id: _Optional[int] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., about: _Optional[str] = ..., avatar: _Optional[str] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...
