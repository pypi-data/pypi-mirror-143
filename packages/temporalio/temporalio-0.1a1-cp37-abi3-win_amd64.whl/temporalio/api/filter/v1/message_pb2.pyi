"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import temporalio.api.enums.v1.workflow_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class WorkflowExecutionFilter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    WORKFLOW_ID_FIELD_NUMBER: builtins.int
    RUN_ID_FIELD_NUMBER: builtins.int
    workflow_id: typing.Text
    run_id: typing.Text
    def __init__(self,
        *,
        workflow_id: typing.Text = ...,
        run_id: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["run_id",b"run_id","workflow_id",b"workflow_id"]) -> None: ...
global___WorkflowExecutionFilter = WorkflowExecutionFilter

class WorkflowTypeFilter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    def __init__(self,
        *,
        name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...
global___WorkflowTypeFilter = WorkflowTypeFilter

class StartTimeFilter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    EARLIEST_TIME_FIELD_NUMBER: builtins.int
    LATEST_TIME_FIELD_NUMBER: builtins.int
    @property
    def earliest_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def latest_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(self,
        *,
        earliest_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        latest_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["earliest_time",b"earliest_time","latest_time",b"latest_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["earliest_time",b"earliest_time","latest_time",b"latest_time"]) -> None: ...
global___StartTimeFilter = StartTimeFilter

class StatusFilter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STATUS_FIELD_NUMBER: builtins.int
    status: temporalio.api.enums.v1.workflow_pb2.WorkflowExecutionStatus.ValueType
    def __init__(self,
        *,
        status: temporalio.api.enums.v1.workflow_pb2.WorkflowExecutionStatus.ValueType = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["status",b"status"]) -> None: ...
global___StatusFilter = StatusFilter
