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

class _QueryResultType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _QueryResultTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_QueryResultType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    QUERY_RESULT_TYPE_UNSPECIFIED: _QueryResultType.ValueType  # 0
    QUERY_RESULT_TYPE_ANSWERED: _QueryResultType.ValueType  # 1
    QUERY_RESULT_TYPE_FAILED: _QueryResultType.ValueType  # 2
class QueryResultType(_QueryResultType, metaclass=_QueryResultTypeEnumTypeWrapper):
    pass

QUERY_RESULT_TYPE_UNSPECIFIED: QueryResultType.ValueType  # 0
QUERY_RESULT_TYPE_ANSWERED: QueryResultType.ValueType  # 1
QUERY_RESULT_TYPE_FAILED: QueryResultType.ValueType  # 2
global___QueryResultType = QueryResultType


class _QueryRejectCondition:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _QueryRejectConditionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_QueryRejectCondition.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    QUERY_REJECT_CONDITION_UNSPECIFIED: _QueryRejectCondition.ValueType  # 0
    QUERY_REJECT_CONDITION_NONE: _QueryRejectCondition.ValueType  # 1
    """None indicates that query should not be rejected."""

    QUERY_REJECT_CONDITION_NOT_OPEN: _QueryRejectCondition.ValueType  # 2
    """NotOpen indicates that query should be rejected if workflow is not open."""

    QUERY_REJECT_CONDITION_NOT_COMPLETED_CLEANLY: _QueryRejectCondition.ValueType  # 3
    """NotCompletedCleanly indicates that query should be rejected if workflow did not complete cleanly."""

class QueryRejectCondition(_QueryRejectCondition, metaclass=_QueryRejectConditionEnumTypeWrapper):
    pass

QUERY_REJECT_CONDITION_UNSPECIFIED: QueryRejectCondition.ValueType  # 0
QUERY_REJECT_CONDITION_NONE: QueryRejectCondition.ValueType  # 1
"""None indicates that query should not be rejected."""

QUERY_REJECT_CONDITION_NOT_OPEN: QueryRejectCondition.ValueType  # 2
"""NotOpen indicates that query should be rejected if workflow is not open."""

QUERY_REJECT_CONDITION_NOT_COMPLETED_CLEANLY: QueryRejectCondition.ValueType  # 3
"""NotCompletedCleanly indicates that query should be rejected if workflow did not complete cleanly."""

global___QueryRejectCondition = QueryRejectCondition

