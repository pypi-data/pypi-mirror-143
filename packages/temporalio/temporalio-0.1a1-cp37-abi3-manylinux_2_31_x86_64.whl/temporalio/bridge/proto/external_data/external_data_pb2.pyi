"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class LocalActivityMarkerData(google.protobuf.message.Message):
    """This file defines data that Core might write externally. The first motivating case being
    storing data in markers in event history. Defining such data as protos provides an easy way
    for consumers which would like to just depend on the proto package to make sense of marker data.

    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SEQ_FIELD_NUMBER: builtins.int
    ATTEMPT_FIELD_NUMBER: builtins.int
    ACTIVITY_ID_FIELD_NUMBER: builtins.int
    ACTIVITY_TYPE_FIELD_NUMBER: builtins.int
    COMPLETE_TIME_FIELD_NUMBER: builtins.int
    BACKOFF_FIELD_NUMBER: builtins.int
    ORIGINAL_SCHEDULE_TIME_FIELD_NUMBER: builtins.int
    seq: builtins.int
    attempt: builtins.int
    """The number of attempts at execution before we recorded this result. Typically starts at 1,
    but it is possible to start at a higher number when backing off using a timer.
    """

    activity_id: typing.Text
    activity_type: typing.Text
    @property
    def complete_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """You can think of this as "perceived completion time". It is the time the local activity thought
        it was when it completed. Which could be different from wall-clock time because of workflow
        replay. It's the WFT start time + the LA's runtime
        """
        pass
    @property
    def backoff(self) -> google.protobuf.duration_pb2.Duration:
        """If set, this local activity conceptually is retrying after the specified backoff.
        Implementation wise, they are really two different LA machines, but with the same type & input.
        The retry starts with an attempt number > 1.
        """
        pass
    @property
    def original_schedule_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The time the LA was originally scheduled (wall clock time). This is used to track
        schedule-to-close timeouts when timer-based backoffs are used
        """
        pass
    def __init__(self,
        *,
        seq: builtins.int = ...,
        attempt: builtins.int = ...,
        activity_id: typing.Text = ...,
        activity_type: typing.Text = ...,
        complete_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        backoff: typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
        original_schedule_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["backoff",b"backoff","complete_time",b"complete_time","original_schedule_time",b"original_schedule_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["activity_id",b"activity_id","activity_type",b"activity_type","attempt",b"attempt","backoff",b"backoff","complete_time",b"complete_time","original_schedule_time",b"original_schedule_time","seq",b"seq"]) -> None: ...
global___LocalActivityMarkerData = LocalActivityMarkerData
