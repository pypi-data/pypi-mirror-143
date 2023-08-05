# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/enums/v1/common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"temporal/api/enums/v1/common.proto\x12\x15temporal.api.enums.v1*_\n\x0c\x45ncodingType\x12\x1d\n\x19\x45NCODING_TYPE_UNSPECIFIED\x10\x00\x12\x18\n\x14\x45NCODING_TYPE_PROTO3\x10\x01\x12\x16\n\x12\x45NCODING_TYPE_JSON\x10\x02*\xec\x01\n\x10IndexedValueType\x12\"\n\x1eINDEXED_VALUE_TYPE_UNSPECIFIED\x10\x00\x12\x1b\n\x17INDEXED_VALUE_TYPE_TEXT\x10\x01\x12\x1e\n\x1aINDEXED_VALUE_TYPE_KEYWORD\x10\x02\x12\x1a\n\x16INDEXED_VALUE_TYPE_INT\x10\x03\x12\x1d\n\x19INDEXED_VALUE_TYPE_DOUBLE\x10\x04\x12\x1b\n\x17INDEXED_VALUE_TYPE_BOOL\x10\x05\x12\x1f\n\x1bINDEXED_VALUE_TYPE_DATETIME\x10\x06*^\n\x08Severity\x12\x18\n\x14SEVERITY_UNSPECIFIED\x10\x00\x12\x11\n\rSEVERITY_HIGH\x10\x01\x12\x13\n\x0fSEVERITY_MEDIUM\x10\x02\x12\x10\n\x0cSEVERITY_LOW\x10\x03\x42\x7f\n\x18io.temporal.api.enums.v1B\x0b\x43ommonProtoP\x01Z!go.temporal.io/api/enums/v1;enums\xaa\x02\x15Temporal.Api.Enums.V1\xea\x02\x18Temporal::Api::Enums::V1b\x06proto3')

_ENCODINGTYPE = DESCRIPTOR.enum_types_by_name['EncodingType']
EncodingType = enum_type_wrapper.EnumTypeWrapper(_ENCODINGTYPE)
_INDEXEDVALUETYPE = DESCRIPTOR.enum_types_by_name['IndexedValueType']
IndexedValueType = enum_type_wrapper.EnumTypeWrapper(_INDEXEDVALUETYPE)
_SEVERITY = DESCRIPTOR.enum_types_by_name['Severity']
Severity = enum_type_wrapper.EnumTypeWrapper(_SEVERITY)
ENCODING_TYPE_UNSPECIFIED = 0
ENCODING_TYPE_PROTO3 = 1
ENCODING_TYPE_JSON = 2
INDEXED_VALUE_TYPE_UNSPECIFIED = 0
INDEXED_VALUE_TYPE_TEXT = 1
INDEXED_VALUE_TYPE_KEYWORD = 2
INDEXED_VALUE_TYPE_INT = 3
INDEXED_VALUE_TYPE_DOUBLE = 4
INDEXED_VALUE_TYPE_BOOL = 5
INDEXED_VALUE_TYPE_DATETIME = 6
SEVERITY_UNSPECIFIED = 0
SEVERITY_HIGH = 1
SEVERITY_MEDIUM = 2
SEVERITY_LOW = 3


if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030io.temporal.api.enums.v1B\013CommonProtoP\001Z!go.temporal.io/api/enums/v1;enums\252\002\025Temporal.Api.Enums.V1\352\002\030Temporal::Api::Enums::V1'
  _ENCODINGTYPE._serialized_start=61
  _ENCODINGTYPE._serialized_end=156
  _INDEXEDVALUETYPE._serialized_start=159
  _INDEXEDVALUETYPE._serialized_end=395
  _SEVERITY._serialized_start=397
  _SEVERITY._serialized_end=491
# @@protoc_insertion_point(module_scope)
