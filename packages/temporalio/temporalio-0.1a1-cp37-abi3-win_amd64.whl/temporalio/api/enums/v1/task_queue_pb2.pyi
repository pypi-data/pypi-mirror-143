"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _TaskQueueKind:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _TaskQueueKindEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TaskQueueKind.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    TASK_QUEUE_KIND_UNSPECIFIED: _TaskQueueKind.ValueType  # 0
    TASK_QUEUE_KIND_NORMAL: _TaskQueueKind.ValueType  # 1
    """Tasks from a normal workflow task queue always include complete workflow history

    The task queue specified by the user is always a normal task queue. There can be as many
    workers as desired for a single normal task queue. All those workers may pick up tasks from
    that queue.
    """

    TASK_QUEUE_KIND_STICKY: _TaskQueueKind.ValueType  # 2
    """A sticky queue only includes new history since the last workflow task, and they are
    per-worker.

    Sticky queues are created dynamically by each worker during their start up. They only exist
    for the lifetime of the worker process. Tasks in a sticky task queue are only available to
    the worker that created the sticky queue.

    Sticky queues are only for workflow tasks. There are no sticky task queues for activities.
    """

class TaskQueueKind(_TaskQueueKind, metaclass=_TaskQueueKindEnumTypeWrapper):
    pass

TASK_QUEUE_KIND_UNSPECIFIED: TaskQueueKind.ValueType  # 0
TASK_QUEUE_KIND_NORMAL: TaskQueueKind.ValueType  # 1
"""Tasks from a normal workflow task queue always include complete workflow history

The task queue specified by the user is always a normal task queue. There can be as many
workers as desired for a single normal task queue. All those workers may pick up tasks from
that queue.
"""

TASK_QUEUE_KIND_STICKY: TaskQueueKind.ValueType  # 2
"""A sticky queue only includes new history since the last workflow task, and they are
per-worker.

Sticky queues are created dynamically by each worker during their start up. They only exist
for the lifetime of the worker process. Tasks in a sticky task queue are only available to
the worker that created the sticky queue.

Sticky queues are only for workflow tasks. There are no sticky task queues for activities.
"""

global___TaskQueueKind = TaskQueueKind


class _TaskQueueType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _TaskQueueTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TaskQueueType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    TASK_QUEUE_TYPE_UNSPECIFIED: _TaskQueueType.ValueType  # 0
    TASK_QUEUE_TYPE_WORKFLOW: _TaskQueueType.ValueType  # 1
    """Workflow type of task queue."""

    TASK_QUEUE_TYPE_ACTIVITY: _TaskQueueType.ValueType  # 2
    """Activity type of task queue."""

class TaskQueueType(_TaskQueueType, metaclass=_TaskQueueTypeEnumTypeWrapper):
    pass

TASK_QUEUE_TYPE_UNSPECIFIED: TaskQueueType.ValueType  # 0
TASK_QUEUE_TYPE_WORKFLOW: TaskQueueType.ValueType  # 1
"""Workflow type of task queue."""

TASK_QUEUE_TYPE_ACTIVITY: TaskQueueType.ValueType  # 2
"""Activity type of task queue."""

global___TaskQueueType = TaskQueueType

