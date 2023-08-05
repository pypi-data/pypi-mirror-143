# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/enums/v1/namespace.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%temporal/api/enums/v1/namespace.proto\x12\x15temporal.api.enums.v1*\x8e\x01\n\x0eNamespaceState\x12\x1f\n\x1bNAMESPACE_STATE_UNSPECIFIED\x10\x00\x12\x1e\n\x1aNAMESPACE_STATE_REGISTERED\x10\x01\x12\x1e\n\x1aNAMESPACE_STATE_DEPRECATED\x10\x02\x12\x1b\n\x17NAMESPACE_STATE_DELETED\x10\x03*h\n\rArchivalState\x12\x1e\n\x1a\x41RCHIVAL_STATE_UNSPECIFIED\x10\x00\x12\x1b\n\x17\x41RCHIVAL_STATE_DISABLED\x10\x01\x12\x1a\n\x16\x41RCHIVAL_STATE_ENABLED\x10\x02*s\n\x10ReplicationState\x12!\n\x1dREPLICATION_STATE_UNSPECIFIED\x10\x00\x12\x1c\n\x18REPLICATION_STATE_NORMAL\x10\x01\x12\x1e\n\x1aREPLICATION_STATE_HANDOVER\x10\x02\x42\x82\x01\n\x18io.temporal.api.enums.v1B\x0eNamespaceProtoP\x01Z!go.temporal.io/api/enums/v1;enums\xaa\x02\x15Temporal.Api.Enums.V1\xea\x02\x18Temporal::Api::Enums::V1b\x06proto3')

_NAMESPACESTATE = DESCRIPTOR.enum_types_by_name['NamespaceState']
NamespaceState = enum_type_wrapper.EnumTypeWrapper(_NAMESPACESTATE)
_ARCHIVALSTATE = DESCRIPTOR.enum_types_by_name['ArchivalState']
ArchivalState = enum_type_wrapper.EnumTypeWrapper(_ARCHIVALSTATE)
_REPLICATIONSTATE = DESCRIPTOR.enum_types_by_name['ReplicationState']
ReplicationState = enum_type_wrapper.EnumTypeWrapper(_REPLICATIONSTATE)
NAMESPACE_STATE_UNSPECIFIED = 0
NAMESPACE_STATE_REGISTERED = 1
NAMESPACE_STATE_DEPRECATED = 2
NAMESPACE_STATE_DELETED = 3
ARCHIVAL_STATE_UNSPECIFIED = 0
ARCHIVAL_STATE_DISABLED = 1
ARCHIVAL_STATE_ENABLED = 2
REPLICATION_STATE_UNSPECIFIED = 0
REPLICATION_STATE_NORMAL = 1
REPLICATION_STATE_HANDOVER = 2


if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030io.temporal.api.enums.v1B\016NamespaceProtoP\001Z!go.temporal.io/api/enums/v1;enums\252\002\025Temporal.Api.Enums.V1\352\002\030Temporal::Api::Enums::V1'
  _NAMESPACESTATE._serialized_start=65
  _NAMESPACESTATE._serialized_end=207
  _ARCHIVALSTATE._serialized_start=209
  _ARCHIVALSTATE._serialized_end=313
  _REPLICATIONSTATE._serialized_start=315
  _REPLICATIONSTATE._serialized_end=430
# @@protoc_insertion_point(module_scope)
