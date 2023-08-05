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

class _WorkflowIdReusePolicy:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _WorkflowIdReusePolicyEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_WorkflowIdReusePolicy.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    WORKFLOW_ID_REUSE_POLICY_UNSPECIFIED: _WorkflowIdReusePolicy.ValueType  # 0
    WORKFLOW_ID_REUSE_POLICY_ALLOW_DUPLICATE: _WorkflowIdReusePolicy.ValueType  # 1
    """Allow starting a workflow execution using the same workflow id."""

    WORKFLOW_ID_REUSE_POLICY_ALLOW_DUPLICATE_FAILED_ONLY: _WorkflowIdReusePolicy.ValueType  # 2
    """Allow starting a workflow execution using the same workflow id, only when the last
    execution's final state is one of [terminated, cancelled, timed out, failed].
    """

    WORKFLOW_ID_REUSE_POLICY_REJECT_DUPLICATE: _WorkflowIdReusePolicy.ValueType  # 3
    """Do not permit re-use of the workflow id for this workflow. Future start workflow requests
    could potentially change the policy, allowing re-use of the workflow id.
    """

class WorkflowIdReusePolicy(_WorkflowIdReusePolicy, metaclass=_WorkflowIdReusePolicyEnumTypeWrapper):
    """Defines how new runs of a workflow with a particular ID may or may not be allowed. Note that
    it is *never* valid to have two actively running instances of the same workflow id.
    """
    pass

WORKFLOW_ID_REUSE_POLICY_UNSPECIFIED: WorkflowIdReusePolicy.ValueType  # 0
WORKFLOW_ID_REUSE_POLICY_ALLOW_DUPLICATE: WorkflowIdReusePolicy.ValueType  # 1
"""Allow starting a workflow execution using the same workflow id."""

WORKFLOW_ID_REUSE_POLICY_ALLOW_DUPLICATE_FAILED_ONLY: WorkflowIdReusePolicy.ValueType  # 2
"""Allow starting a workflow execution using the same workflow id, only when the last
execution's final state is one of [terminated, cancelled, timed out, failed].
"""

WORKFLOW_ID_REUSE_POLICY_REJECT_DUPLICATE: WorkflowIdReusePolicy.ValueType  # 3
"""Do not permit re-use of the workflow id for this workflow. Future start workflow requests
could potentially change the policy, allowing re-use of the workflow id.
"""

global___WorkflowIdReusePolicy = WorkflowIdReusePolicy


class _ParentClosePolicy:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ParentClosePolicyEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ParentClosePolicy.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PARENT_CLOSE_POLICY_UNSPECIFIED: _ParentClosePolicy.ValueType  # 0
    PARENT_CLOSE_POLICY_TERMINATE: _ParentClosePolicy.ValueType  # 1
    """The child workflow will also terminate"""

    PARENT_CLOSE_POLICY_ABANDON: _ParentClosePolicy.ValueType  # 2
    """The child workflow will do nothing"""

    PARENT_CLOSE_POLICY_REQUEST_CANCEL: _ParentClosePolicy.ValueType  # 3
    """Cancellation will be requested of the child workflow"""

class ParentClosePolicy(_ParentClosePolicy, metaclass=_ParentClosePolicyEnumTypeWrapper):
    """Defines how child workflows will react to their parent completing"""
    pass

PARENT_CLOSE_POLICY_UNSPECIFIED: ParentClosePolicy.ValueType  # 0
PARENT_CLOSE_POLICY_TERMINATE: ParentClosePolicy.ValueType  # 1
"""The child workflow will also terminate"""

PARENT_CLOSE_POLICY_ABANDON: ParentClosePolicy.ValueType  # 2
"""The child workflow will do nothing"""

PARENT_CLOSE_POLICY_REQUEST_CANCEL: ParentClosePolicy.ValueType  # 3
"""Cancellation will be requested of the child workflow"""

global___ParentClosePolicy = ParentClosePolicy


class _ContinueAsNewInitiator:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ContinueAsNewInitiatorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ContinueAsNewInitiator.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CONTINUE_AS_NEW_INITIATOR_UNSPECIFIED: _ContinueAsNewInitiator.ValueType  # 0
    CONTINUE_AS_NEW_INITIATOR_WORKFLOW: _ContinueAsNewInitiator.ValueType  # 1
    """The workflow itself requested to continue as new"""

    CONTINUE_AS_NEW_INITIATOR_RETRY: _ContinueAsNewInitiator.ValueType  # 2
    """The workflow continued as new because it is retrying"""

    CONTINUE_AS_NEW_INITIATOR_CRON_SCHEDULE: _ContinueAsNewInitiator.ValueType  # 3
    """The workflow continued as new because cron has triggered a new execution"""

class ContinueAsNewInitiator(_ContinueAsNewInitiator, metaclass=_ContinueAsNewInitiatorEnumTypeWrapper):
    pass

CONTINUE_AS_NEW_INITIATOR_UNSPECIFIED: ContinueAsNewInitiator.ValueType  # 0
CONTINUE_AS_NEW_INITIATOR_WORKFLOW: ContinueAsNewInitiator.ValueType  # 1
"""The workflow itself requested to continue as new"""

CONTINUE_AS_NEW_INITIATOR_RETRY: ContinueAsNewInitiator.ValueType  # 2
"""The workflow continued as new because it is retrying"""

CONTINUE_AS_NEW_INITIATOR_CRON_SCHEDULE: ContinueAsNewInitiator.ValueType  # 3
"""The workflow continued as new because cron has triggered a new execution"""

global___ContinueAsNewInitiator = ContinueAsNewInitiator


class _WorkflowExecutionStatus:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _WorkflowExecutionStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_WorkflowExecutionStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    WORKFLOW_EXECUTION_STATUS_UNSPECIFIED: _WorkflowExecutionStatus.ValueType  # 0
    WORKFLOW_EXECUTION_STATUS_RUNNING: _WorkflowExecutionStatus.ValueType  # 1
    """Value 1 is hardcoded in SQL persistence."""

    WORKFLOW_EXECUTION_STATUS_COMPLETED: _WorkflowExecutionStatus.ValueType  # 2
    WORKFLOW_EXECUTION_STATUS_FAILED: _WorkflowExecutionStatus.ValueType  # 3
    WORKFLOW_EXECUTION_STATUS_CANCELED: _WorkflowExecutionStatus.ValueType  # 4
    WORKFLOW_EXECUTION_STATUS_TERMINATED: _WorkflowExecutionStatus.ValueType  # 5
    WORKFLOW_EXECUTION_STATUS_CONTINUED_AS_NEW: _WorkflowExecutionStatus.ValueType  # 6
    WORKFLOW_EXECUTION_STATUS_TIMED_OUT: _WorkflowExecutionStatus.ValueType  # 7
class WorkflowExecutionStatus(_WorkflowExecutionStatus, metaclass=_WorkflowExecutionStatusEnumTypeWrapper):
    """(-- api-linter: core::0216::synonyms=disabled
        aip.dev/not-precedent: There is WorkflowExecutionState already in another package. --)
    """
    pass

WORKFLOW_EXECUTION_STATUS_UNSPECIFIED: WorkflowExecutionStatus.ValueType  # 0
WORKFLOW_EXECUTION_STATUS_RUNNING: WorkflowExecutionStatus.ValueType  # 1
"""Value 1 is hardcoded in SQL persistence."""

WORKFLOW_EXECUTION_STATUS_COMPLETED: WorkflowExecutionStatus.ValueType  # 2
WORKFLOW_EXECUTION_STATUS_FAILED: WorkflowExecutionStatus.ValueType  # 3
WORKFLOW_EXECUTION_STATUS_CANCELED: WorkflowExecutionStatus.ValueType  # 4
WORKFLOW_EXECUTION_STATUS_TERMINATED: WorkflowExecutionStatus.ValueType  # 5
WORKFLOW_EXECUTION_STATUS_CONTINUED_AS_NEW: WorkflowExecutionStatus.ValueType  # 6
WORKFLOW_EXECUTION_STATUS_TIMED_OUT: WorkflowExecutionStatus.ValueType  # 7
global___WorkflowExecutionStatus = WorkflowExecutionStatus


class _PendingActivityState:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _PendingActivityStateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PendingActivityState.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PENDING_ACTIVITY_STATE_UNSPECIFIED: _PendingActivityState.ValueType  # 0
    PENDING_ACTIVITY_STATE_SCHEDULED: _PendingActivityState.ValueType  # 1
    PENDING_ACTIVITY_STATE_STARTED: _PendingActivityState.ValueType  # 2
    PENDING_ACTIVITY_STATE_CANCEL_REQUESTED: _PendingActivityState.ValueType  # 3
class PendingActivityState(_PendingActivityState, metaclass=_PendingActivityStateEnumTypeWrapper):
    pass

PENDING_ACTIVITY_STATE_UNSPECIFIED: PendingActivityState.ValueType  # 0
PENDING_ACTIVITY_STATE_SCHEDULED: PendingActivityState.ValueType  # 1
PENDING_ACTIVITY_STATE_STARTED: PendingActivityState.ValueType  # 2
PENDING_ACTIVITY_STATE_CANCEL_REQUESTED: PendingActivityState.ValueType  # 3
global___PendingActivityState = PendingActivityState


class _PendingWorkflowTaskState:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _PendingWorkflowTaskStateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PendingWorkflowTaskState.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PENDING_WORKFLOW_TASK_STATE_UNSPECIFIED: _PendingWorkflowTaskState.ValueType  # 0
    PENDING_WORKFLOW_TASK_STATE_SCHEDULED: _PendingWorkflowTaskState.ValueType  # 1
    PENDING_WORKFLOW_TASK_STATE_STARTED: _PendingWorkflowTaskState.ValueType  # 2
class PendingWorkflowTaskState(_PendingWorkflowTaskState, metaclass=_PendingWorkflowTaskStateEnumTypeWrapper):
    pass

PENDING_WORKFLOW_TASK_STATE_UNSPECIFIED: PendingWorkflowTaskState.ValueType  # 0
PENDING_WORKFLOW_TASK_STATE_SCHEDULED: PendingWorkflowTaskState.ValueType  # 1
PENDING_WORKFLOW_TASK_STATE_STARTED: PendingWorkflowTaskState.ValueType  # 2
global___PendingWorkflowTaskState = PendingWorkflowTaskState


class _HistoryEventFilterType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _HistoryEventFilterTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_HistoryEventFilterType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    HISTORY_EVENT_FILTER_TYPE_UNSPECIFIED: _HistoryEventFilterType.ValueType  # 0
    HISTORY_EVENT_FILTER_TYPE_ALL_EVENT: _HistoryEventFilterType.ValueType  # 1
    HISTORY_EVENT_FILTER_TYPE_CLOSE_EVENT: _HistoryEventFilterType.ValueType  # 2
class HistoryEventFilterType(_HistoryEventFilterType, metaclass=_HistoryEventFilterTypeEnumTypeWrapper):
    pass

HISTORY_EVENT_FILTER_TYPE_UNSPECIFIED: HistoryEventFilterType.ValueType  # 0
HISTORY_EVENT_FILTER_TYPE_ALL_EVENT: HistoryEventFilterType.ValueType  # 1
HISTORY_EVENT_FILTER_TYPE_CLOSE_EVENT: HistoryEventFilterType.ValueType  # 2
global___HistoryEventFilterType = HistoryEventFilterType


class _RetryState:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _RetryStateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_RetryState.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    RETRY_STATE_UNSPECIFIED: _RetryState.ValueType  # 0
    RETRY_STATE_IN_PROGRESS: _RetryState.ValueType  # 1
    RETRY_STATE_NON_RETRYABLE_FAILURE: _RetryState.ValueType  # 2
    RETRY_STATE_TIMEOUT: _RetryState.ValueType  # 3
    RETRY_STATE_MAXIMUM_ATTEMPTS_REACHED: _RetryState.ValueType  # 4
    RETRY_STATE_RETRY_POLICY_NOT_SET: _RetryState.ValueType  # 5
    RETRY_STATE_INTERNAL_SERVER_ERROR: _RetryState.ValueType  # 6
    RETRY_STATE_CANCEL_REQUESTED: _RetryState.ValueType  # 7
class RetryState(_RetryState, metaclass=_RetryStateEnumTypeWrapper):
    pass

RETRY_STATE_UNSPECIFIED: RetryState.ValueType  # 0
RETRY_STATE_IN_PROGRESS: RetryState.ValueType  # 1
RETRY_STATE_NON_RETRYABLE_FAILURE: RetryState.ValueType  # 2
RETRY_STATE_TIMEOUT: RetryState.ValueType  # 3
RETRY_STATE_MAXIMUM_ATTEMPTS_REACHED: RetryState.ValueType  # 4
RETRY_STATE_RETRY_POLICY_NOT_SET: RetryState.ValueType  # 5
RETRY_STATE_INTERNAL_SERVER_ERROR: RetryState.ValueType  # 6
RETRY_STATE_CANCEL_REQUESTED: RetryState.ValueType  # 7
global___RetryState = RetryState


class _TimeoutType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _TimeoutTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TimeoutType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    TIMEOUT_TYPE_UNSPECIFIED: _TimeoutType.ValueType  # 0
    TIMEOUT_TYPE_START_TO_CLOSE: _TimeoutType.ValueType  # 1
    TIMEOUT_TYPE_SCHEDULE_TO_START: _TimeoutType.ValueType  # 2
    TIMEOUT_TYPE_SCHEDULE_TO_CLOSE: _TimeoutType.ValueType  # 3
    TIMEOUT_TYPE_HEARTBEAT: _TimeoutType.ValueType  # 4
class TimeoutType(_TimeoutType, metaclass=_TimeoutTypeEnumTypeWrapper):
    pass

TIMEOUT_TYPE_UNSPECIFIED: TimeoutType.ValueType  # 0
TIMEOUT_TYPE_START_TO_CLOSE: TimeoutType.ValueType  # 1
TIMEOUT_TYPE_SCHEDULE_TO_START: TimeoutType.ValueType  # 2
TIMEOUT_TYPE_SCHEDULE_TO_CLOSE: TimeoutType.ValueType  # 3
TIMEOUT_TYPE_HEARTBEAT: TimeoutType.ValueType  # 4
global___TimeoutType = TimeoutType

