# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/errordetails/v1/message.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from temporalio.api.enums.v1 import failed_cause_pb2 as temporal_dot_api_dot_enums_dot_v1_dot_failed__cause__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*temporal/api/errordetails/v1/message.proto\x12\x1ctemporal.api.errordetails.v1\x1a(temporal/api/enums/v1/failed_cause.proto\"B\n\x0fNotFoundFailure\x12\x17\n\x0f\x63urrent_cluster\x18\x01 \x01(\t\x12\x16\n\x0e\x61\x63tive_cluster\x18\x02 \x01(\t\"R\n&WorkflowExecutionAlreadyStartedFailure\x12\x18\n\x10start_request_id\x18\x01 \x01(\t\x12\x0e\n\x06run_id\x18\x02 \x01(\t\"_\n\x19NamespaceNotActiveFailure\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x17\n\x0f\x63urrent_cluster\x18\x02 \x01(\t\x12\x16\n\x0e\x61\x63tive_cluster\x18\x03 \x01(\t\"k\n ClientVersionNotSupportedFailure\x12\x16\n\x0e\x63lient_version\x18\x01 \x01(\t\x12\x13\n\x0b\x63lient_name\x18\x02 \x01(\t\x12\x1a\n\x12supported_versions\x18\x03 \x01(\t\"d\n ServerVersionNotSupportedFailure\x12\x16\n\x0eserver_version\x18\x01 \x01(\t\x12(\n client_supported_server_versions\x18\x02 \x01(\t\"\x1f\n\x1dNamespaceAlreadyExistsFailure\"%\n#CancellationAlreadyRequestedFailure\"\x14\n\x12QueryFailedFailure\")\n\x17PermissionDeniedFailure\x12\x0e\n\x06reason\x18\x01 \x01(\t\"X\n\x18ResourceExhaustedFailure\x12<\n\x05\x63\x61use\x18\x01 \x01(\x0e\x32-.temporal.api.enums.v1.ResourceExhaustedCauseB\xa3\x01\n\x1fio.temporal.api.errordetails.v1B\x0cMessageProtoP\x01Z/go.temporal.io/api/errordetails/v1;errordetails\xaa\x02\x1cTemporal.Api.ErrorDetails.V1\xea\x02\x1fTemporal::Api::ErrorDetails::V1b\x06proto3')



_NOTFOUNDFAILURE = DESCRIPTOR.message_types_by_name['NotFoundFailure']
_WORKFLOWEXECUTIONALREADYSTARTEDFAILURE = DESCRIPTOR.message_types_by_name['WorkflowExecutionAlreadyStartedFailure']
_NAMESPACENOTACTIVEFAILURE = DESCRIPTOR.message_types_by_name['NamespaceNotActiveFailure']
_CLIENTVERSIONNOTSUPPORTEDFAILURE = DESCRIPTOR.message_types_by_name['ClientVersionNotSupportedFailure']
_SERVERVERSIONNOTSUPPORTEDFAILURE = DESCRIPTOR.message_types_by_name['ServerVersionNotSupportedFailure']
_NAMESPACEALREADYEXISTSFAILURE = DESCRIPTOR.message_types_by_name['NamespaceAlreadyExistsFailure']
_CANCELLATIONALREADYREQUESTEDFAILURE = DESCRIPTOR.message_types_by_name['CancellationAlreadyRequestedFailure']
_QUERYFAILEDFAILURE = DESCRIPTOR.message_types_by_name['QueryFailedFailure']
_PERMISSIONDENIEDFAILURE = DESCRIPTOR.message_types_by_name['PermissionDeniedFailure']
_RESOURCEEXHAUSTEDFAILURE = DESCRIPTOR.message_types_by_name['ResourceExhaustedFailure']
NotFoundFailure = _reflection.GeneratedProtocolMessageType('NotFoundFailure', (_message.Message,), {
  'DESCRIPTOR' : _NOTFOUNDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.NotFoundFailure)
  })
_sym_db.RegisterMessage(NotFoundFailure)

WorkflowExecutionAlreadyStartedFailure = _reflection.GeneratedProtocolMessageType('WorkflowExecutionAlreadyStartedFailure', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWEXECUTIONALREADYSTARTEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.WorkflowExecutionAlreadyStartedFailure)
  })
_sym_db.RegisterMessage(WorkflowExecutionAlreadyStartedFailure)

NamespaceNotActiveFailure = _reflection.GeneratedProtocolMessageType('NamespaceNotActiveFailure', (_message.Message,), {
  'DESCRIPTOR' : _NAMESPACENOTACTIVEFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.NamespaceNotActiveFailure)
  })
_sym_db.RegisterMessage(NamespaceNotActiveFailure)

ClientVersionNotSupportedFailure = _reflection.GeneratedProtocolMessageType('ClientVersionNotSupportedFailure', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTVERSIONNOTSUPPORTEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.ClientVersionNotSupportedFailure)
  })
_sym_db.RegisterMessage(ClientVersionNotSupportedFailure)

ServerVersionNotSupportedFailure = _reflection.GeneratedProtocolMessageType('ServerVersionNotSupportedFailure', (_message.Message,), {
  'DESCRIPTOR' : _SERVERVERSIONNOTSUPPORTEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.ServerVersionNotSupportedFailure)
  })
_sym_db.RegisterMessage(ServerVersionNotSupportedFailure)

NamespaceAlreadyExistsFailure = _reflection.GeneratedProtocolMessageType('NamespaceAlreadyExistsFailure', (_message.Message,), {
  'DESCRIPTOR' : _NAMESPACEALREADYEXISTSFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.NamespaceAlreadyExistsFailure)
  })
_sym_db.RegisterMessage(NamespaceAlreadyExistsFailure)

CancellationAlreadyRequestedFailure = _reflection.GeneratedProtocolMessageType('CancellationAlreadyRequestedFailure', (_message.Message,), {
  'DESCRIPTOR' : _CANCELLATIONALREADYREQUESTEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.CancellationAlreadyRequestedFailure)
  })
_sym_db.RegisterMessage(CancellationAlreadyRequestedFailure)

QueryFailedFailure = _reflection.GeneratedProtocolMessageType('QueryFailedFailure', (_message.Message,), {
  'DESCRIPTOR' : _QUERYFAILEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.QueryFailedFailure)
  })
_sym_db.RegisterMessage(QueryFailedFailure)

PermissionDeniedFailure = _reflection.GeneratedProtocolMessageType('PermissionDeniedFailure', (_message.Message,), {
  'DESCRIPTOR' : _PERMISSIONDENIEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.PermissionDeniedFailure)
  })
_sym_db.RegisterMessage(PermissionDeniedFailure)

ResourceExhaustedFailure = _reflection.GeneratedProtocolMessageType('ResourceExhaustedFailure', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCEEXHAUSTEDFAILURE,
  '__module__' : 'temporal.api.errordetails.v1.message_pb2'
  # @@protoc_insertion_point(class_scope:temporal.api.errordetails.v1.ResourceExhaustedFailure)
  })
_sym_db.RegisterMessage(ResourceExhaustedFailure)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037io.temporal.api.errordetails.v1B\014MessageProtoP\001Z/go.temporal.io/api/errordetails/v1;errordetails\252\002\034Temporal.Api.ErrorDetails.V1\352\002\037Temporal::Api::ErrorDetails::V1'
  _NOTFOUNDFAILURE._serialized_start=118
  _NOTFOUNDFAILURE._serialized_end=184
  _WORKFLOWEXECUTIONALREADYSTARTEDFAILURE._serialized_start=186
  _WORKFLOWEXECUTIONALREADYSTARTEDFAILURE._serialized_end=268
  _NAMESPACENOTACTIVEFAILURE._serialized_start=270
  _NAMESPACENOTACTIVEFAILURE._serialized_end=365
  _CLIENTVERSIONNOTSUPPORTEDFAILURE._serialized_start=367
  _CLIENTVERSIONNOTSUPPORTEDFAILURE._serialized_end=474
  _SERVERVERSIONNOTSUPPORTEDFAILURE._serialized_start=476
  _SERVERVERSIONNOTSUPPORTEDFAILURE._serialized_end=576
  _NAMESPACEALREADYEXISTSFAILURE._serialized_start=578
  _NAMESPACEALREADYEXISTSFAILURE._serialized_end=609
  _CANCELLATIONALREADYREQUESTEDFAILURE._serialized_start=611
  _CANCELLATIONALREADYREQUESTEDFAILURE._serialized_end=648
  _QUERYFAILEDFAILURE._serialized_start=650
  _QUERYFAILEDFAILURE._serialized_end=670
  _PERMISSIONDENIEDFAILURE._serialized_start=672
  _PERMISSIONDENIEDFAILURE._serialized_end=713
  _RESOURCEEXHAUSTEDFAILURE._serialized_start=715
  _RESOURCEEXHAUSTEDFAILURE._serialized_end=803
# @@protoc_insertion_point(module_scope)
