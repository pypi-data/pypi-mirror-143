# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/enums/v1/query.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!temporal/api/enums/v1/query.proto\x12\x15temporal.api.enums.v1*r\n\x0fQueryResultType\x12!\n\x1dQUERY_RESULT_TYPE_UNSPECIFIED\x10\x00\x12\x1e\n\x1aQUERY_RESULT_TYPE_ANSWERED\x10\x01\x12\x1c\n\x18QUERY_RESULT_TYPE_FAILED\x10\x02*\xb6\x01\n\x14QueryRejectCondition\x12&\n\"QUERY_REJECT_CONDITION_UNSPECIFIED\x10\x00\x12\x1f\n\x1bQUERY_REJECT_CONDITION_NONE\x10\x01\x12#\n\x1fQUERY_REJECT_CONDITION_NOT_OPEN\x10\x02\x12\x30\n,QUERY_REJECT_CONDITION_NOT_COMPLETED_CLEANLY\x10\x03\x42~\n\x18io.temporal.api.enums.v1B\nQueryProtoP\x01Z!go.temporal.io/api/enums/v1;enums\xaa\x02\x15Temporal.Api.Enums.V1\xea\x02\x18Temporal::Api::Enums::V1b\x06proto3')

_QUERYRESULTTYPE = DESCRIPTOR.enum_types_by_name['QueryResultType']
QueryResultType = enum_type_wrapper.EnumTypeWrapper(_QUERYRESULTTYPE)
_QUERYREJECTCONDITION = DESCRIPTOR.enum_types_by_name['QueryRejectCondition']
QueryRejectCondition = enum_type_wrapper.EnumTypeWrapper(_QUERYREJECTCONDITION)
QUERY_RESULT_TYPE_UNSPECIFIED = 0
QUERY_RESULT_TYPE_ANSWERED = 1
QUERY_RESULT_TYPE_FAILED = 2
QUERY_REJECT_CONDITION_UNSPECIFIED = 0
QUERY_REJECT_CONDITION_NONE = 1
QUERY_REJECT_CONDITION_NOT_OPEN = 2
QUERY_REJECT_CONDITION_NOT_COMPLETED_CLEANLY = 3


if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030io.temporal.api.enums.v1B\nQueryProtoP\001Z!go.temporal.io/api/enums/v1;enums\252\002\025Temporal.Api.Enums.V1\352\002\030Temporal::Api::Enums::V1'
  _QUERYRESULTTYPE._serialized_start=60
  _QUERYRESULTTYPE._serialized_end=174
  _QUERYREJECTCONDITION._serialized_start=177
  _QUERYREJECTCONDITION._serialized_end=359
# @@protoc_insertion_point(module_scope)
