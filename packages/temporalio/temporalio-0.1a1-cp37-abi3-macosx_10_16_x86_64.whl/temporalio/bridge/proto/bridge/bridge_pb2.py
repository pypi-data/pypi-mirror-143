# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/sdk/core/bridge/bridge.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from temporal.sdk.core import core_interface_pb2 as temporal_dot_sdk_dot_core_dot_core__interface__pb2
from temporalio.bridge.proto.activity_task import activity_task_pb2 as temporal_dot_sdk_dot_core_dot_activity__task_dot_activity__task__pb2
from temporalio.bridge.proto.workflow_activation import workflow_activation_pb2 as temporal_dot_sdk_dot_core_dot_workflow__activation_dot_workflow__activation__pb2
from temporalio.bridge.proto.workflow_completion import workflow_completion_pb2 as temporal_dot_sdk_dot_core_dot_workflow__completion_dot_workflow__completion__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%temporal/sdk/core/bridge/bridge.proto\x12\x0e\x63oresdk.bridge\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a&temporal/sdk/core/core_interface.proto\x1a\x33temporal/sdk/core/activity_task/activity_task.proto\x1a?temporal/sdk/core/workflow_activation/workflow_activation.proto\x1a?temporal/sdk/core/workflow_completion/workflow_completion.proto\"\xaa\x01\n\x14InitTelemetryRequest\x12\x1a\n\x12otel_collector_url\x18\x01 \x01(\t\x12\x16\n\x0etracing_filter\x18\x02 \x01(\t\x12\x36\n\x14log_forwarding_level\x18\x03 \x01(\x0e\x32\x18.coresdk.bridge.LogLevel\x12&\n\x1eprometheus_export_bind_address\x18\x04 \x01(\t\"\xe0\x06\n\x14\x43reateGatewayRequest\x12\x12\n\ntarget_url\x18\x01 \x01(\t\x12\x11\n\tnamespace\x18\x02 \x01(\t\x12\x13\n\x0b\x63lient_name\x18\x03 \x01(\t\x12\x16\n\x0e\x63lient_version\x18\x04 \x01(\t\x12O\n\x0estatic_headers\x18\x05 \x03(\x0b\x32\x37.coresdk.bridge.CreateGatewayRequest.StaticHeadersEntry\x12\x10\n\x08identity\x18\x06 \x01(\t\x12\x18\n\x10worker_binary_id\x18\x07 \x01(\t\x12\x42\n\ntls_config\x18\x08 \x01(\x0b\x32..coresdk.bridge.CreateGatewayRequest.TlsConfig\x12\x46\n\x0cretry_config\x18\t \x01(\x0b\x32\x30.coresdk.bridge.CreateGatewayRequest.RetryConfig\x1a\x34\n\x12StaticHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1ai\n\tTlsConfig\x12\x1b\n\x13server_root_ca_cert\x18\x01 \x01(\x0c\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x12\x13\n\x0b\x63lient_cert\x18\x03 \x01(\x0c\x12\x1a\n\x12\x63lient_private_key\x18\x04 \x01(\x0c\x1a\xc9\x02\n\x0bRetryConfig\x12\x33\n\x10initial_interval\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration\x12:\n\x14randomization_factor\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x30\n\nmultiplier\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12/\n\x0cmax_interval\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x33\n\x10max_elapsed_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x31\n\x0bmax_retries\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\"[\n\x0cInitResponse\x12\x31\n\x05\x65rror\x18\x01 \x01(\x0b\x32\".coresdk.bridge.InitResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"\xee\x05\n\x13\x43reateWorkerRequest\x12\x12\n\ntask_queue\x18\x01 \x01(\t\x12:\n\x14max_cached_workflows\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x44\n\x1emax_outstanding_workflow_tasks\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12@\n\x1amax_outstanding_activities\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x46\n max_outstanding_local_activities\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12>\n\x18max_concurrent_wft_polls\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x43\n\x1enonsticky_to_sticky_poll_ratio\x18\x07 \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12=\n\x17max_concurrent_at_polls\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x1c\n\x14no_remote_activities\x18\t \x01(\x08\x12I\n&sticky_queue_schedule_to_start_timeout\x18\n \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x42\n\x1fmax_heartbeat_throttle_interval\x18\x0b \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x46\n#default_heartbeat_throttle_interval\x18\x0c \x01(\x0b\x32\x19.google.protobuf.Duration\"o\n\x16RegisterWorkerResponse\x12;\n\x05\x65rror\x18\x01 \x01(\x0b\x32,.coresdk.bridge.RegisterWorkerResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\x1dPollWorkflowActivationRequest\"\xe6\x01\n\x1ePollWorkflowActivationResponse\x12\x45\n\nactivation\x18\x01 \x01(\x0b\x32/.coresdk.workflow_activation.WorkflowActivationH\x00\x12\x45\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x34.coresdk.bridge.PollWorkflowActivationResponse.ErrorH\x00\x1a*\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x10\n\x08shutdown\x18\x02 \x01(\x08\x42\n\n\x08response\"\x19\n\x17PollActivityTaskRequest\"\xc8\x01\n\x18PollActivityTaskResponse\x12\x33\n\x04task\x18\x01 \x01(\x0b\x32#.coresdk.activity_task.ActivityTaskH\x00\x12?\n\x05\x65rror\x18\x02 \x01(\x0b\x32..coresdk.bridge.PollActivityTaskResponse.ErrorH\x00\x1a*\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x10\n\x08shutdown\x18\x02 \x01(\x08\x42\n\n\x08response\"r\n!CompleteWorkflowActivationRequest\x12M\n\ncompletion\x18\x01 \x01(\x0b\x32\x39.coresdk.workflow_completion.WorkflowActivationCompletion\"\x87\x01\n\"CompleteWorkflowActivationResponse\x12G\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x38.coresdk.bridge.CompleteWorkflowActivationResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"R\n\x1b\x43ompleteActivityTaskRequest\x12\x33\n\ncompletion\x18\x01 \x01(\x0b\x32\x1f.coresdk.ActivityTaskCompletion\"{\n\x1c\x43ompleteActivityTaskResponse\x12\x41\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x32.coresdk.bridge.CompleteActivityTaskResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"O\n\x1eRecordActivityHeartbeatRequest\x12-\n\theartbeat\x18\x01 \x01(\x0b\x32\x1a.coresdk.ActivityHeartbeat\"\x81\x01\n\x1fRecordActivityHeartbeatResponse\x12\x44\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x35.coresdk.bridge.RecordActivityHeartbeatResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"0\n\x1eRequestWorkflowEvictionRequest\x12\x0e\n\x06run_id\x18\x01 \x01(\t\"\x81\x01\n\x1fRequestWorkflowEvictionResponse\x12\x44\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x35.coresdk.bridge.RequestWorkflowEvictionResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x17\n\x15ShutdownWorkerRequest\"o\n\x16ShutdownWorkerResponse\x12;\n\x05\x65rror\x18\x01 \x01(\x0b\x32,.coresdk.bridge.ShutdownWorkerResponse.Error\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1a\n\x18\x46\x65tchBufferedLogsRequest\"\xd5\x01\n\x19\x46\x65tchBufferedLogsResponse\x12\x43\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x32.coresdk.bridge.FetchBufferedLogsResponse.LogEntry\x1as\n\x08LogEntry\x12\x0f\n\x07message\x18\x01 \x01(\t\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x05level\x18\x03 \x01(\x0e\x32\x18.coresdk.bridge.LogLevel*c\n\x08LogLevel\x12\x19\n\x15LOG_LEVEL_UNSPECIFIED\x10\x00\x12\x07\n\x03OFF\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x12\x08\n\x04WARN\x10\x03\x12\x08\n\x04INFO\x10\x04\x12\t\n\x05\x44\x45\x42UG\x10\x05\x12\t\n\x05TRACE\x10\x06\x62\x06proto3')

_LOGLEVEL = DESCRIPTOR.enum_types_by_name['LogLevel']
LogLevel = enum_type_wrapper.EnumTypeWrapper(_LOGLEVEL)
LOG_LEVEL_UNSPECIFIED = 0
OFF = 1
ERROR = 2
WARN = 3
INFO = 4
DEBUG = 5
TRACE = 6


_INITTELEMETRYREQUEST = DESCRIPTOR.message_types_by_name['InitTelemetryRequest']
_CREATEGATEWAYREQUEST = DESCRIPTOR.message_types_by_name['CreateGatewayRequest']
_CREATEGATEWAYREQUEST_STATICHEADERSENTRY = _CREATEGATEWAYREQUEST.nested_types_by_name['StaticHeadersEntry']
_CREATEGATEWAYREQUEST_TLSCONFIG = _CREATEGATEWAYREQUEST.nested_types_by_name['TlsConfig']
_CREATEGATEWAYREQUEST_RETRYCONFIG = _CREATEGATEWAYREQUEST.nested_types_by_name['RetryConfig']
_INITRESPONSE = DESCRIPTOR.message_types_by_name['InitResponse']
_INITRESPONSE_ERROR = _INITRESPONSE.nested_types_by_name['Error']
_CREATEWORKERREQUEST = DESCRIPTOR.message_types_by_name['CreateWorkerRequest']
_REGISTERWORKERRESPONSE = DESCRIPTOR.message_types_by_name['RegisterWorkerResponse']
_REGISTERWORKERRESPONSE_ERROR = _REGISTERWORKERRESPONSE.nested_types_by_name['Error']
_POLLWORKFLOWACTIVATIONREQUEST = DESCRIPTOR.message_types_by_name['PollWorkflowActivationRequest']
_POLLWORKFLOWACTIVATIONRESPONSE = DESCRIPTOR.message_types_by_name['PollWorkflowActivationResponse']
_POLLWORKFLOWACTIVATIONRESPONSE_ERROR = _POLLWORKFLOWACTIVATIONRESPONSE.nested_types_by_name['Error']
_POLLACTIVITYTASKREQUEST = DESCRIPTOR.message_types_by_name['PollActivityTaskRequest']
_POLLACTIVITYTASKRESPONSE = DESCRIPTOR.message_types_by_name['PollActivityTaskResponse']
_POLLACTIVITYTASKRESPONSE_ERROR = _POLLACTIVITYTASKRESPONSE.nested_types_by_name['Error']
_COMPLETEWORKFLOWACTIVATIONREQUEST = DESCRIPTOR.message_types_by_name['CompleteWorkflowActivationRequest']
_COMPLETEWORKFLOWACTIVATIONRESPONSE = DESCRIPTOR.message_types_by_name['CompleteWorkflowActivationResponse']
_COMPLETEWORKFLOWACTIVATIONRESPONSE_ERROR = _COMPLETEWORKFLOWACTIVATIONRESPONSE.nested_types_by_name['Error']
_COMPLETEACTIVITYTASKREQUEST = DESCRIPTOR.message_types_by_name['CompleteActivityTaskRequest']
_COMPLETEACTIVITYTASKRESPONSE = DESCRIPTOR.message_types_by_name['CompleteActivityTaskResponse']
_COMPLETEACTIVITYTASKRESPONSE_ERROR = _COMPLETEACTIVITYTASKRESPONSE.nested_types_by_name['Error']
_RECORDACTIVITYHEARTBEATREQUEST = DESCRIPTOR.message_types_by_name['RecordActivityHeartbeatRequest']
_RECORDACTIVITYHEARTBEATRESPONSE = DESCRIPTOR.message_types_by_name['RecordActivityHeartbeatResponse']
_RECORDACTIVITYHEARTBEATRESPONSE_ERROR = _RECORDACTIVITYHEARTBEATRESPONSE.nested_types_by_name['Error']
_REQUESTWORKFLOWEVICTIONREQUEST = DESCRIPTOR.message_types_by_name['RequestWorkflowEvictionRequest']
_REQUESTWORKFLOWEVICTIONRESPONSE = DESCRIPTOR.message_types_by_name['RequestWorkflowEvictionResponse']
_REQUESTWORKFLOWEVICTIONRESPONSE_ERROR = _REQUESTWORKFLOWEVICTIONRESPONSE.nested_types_by_name['Error']
_SHUTDOWNWORKERREQUEST = DESCRIPTOR.message_types_by_name['ShutdownWorkerRequest']
_SHUTDOWNWORKERRESPONSE = DESCRIPTOR.message_types_by_name['ShutdownWorkerResponse']
_SHUTDOWNWORKERRESPONSE_ERROR = _SHUTDOWNWORKERRESPONSE.nested_types_by_name['Error']
_FETCHBUFFEREDLOGSREQUEST = DESCRIPTOR.message_types_by_name['FetchBufferedLogsRequest']
_FETCHBUFFEREDLOGSRESPONSE = DESCRIPTOR.message_types_by_name['FetchBufferedLogsResponse']
_FETCHBUFFEREDLOGSRESPONSE_LOGENTRY = _FETCHBUFFEREDLOGSRESPONSE.nested_types_by_name['LogEntry']
InitTelemetryRequest = _reflection.GeneratedProtocolMessageType('InitTelemetryRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITTELEMETRYREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.InitTelemetryRequest)
  })
_sym_db.RegisterMessage(InitTelemetryRequest)

CreateGatewayRequest = _reflection.GeneratedProtocolMessageType('CreateGatewayRequest', (_message.Message,), {

  'StaticHeadersEntry' : _reflection.GeneratedProtocolMessageType('StaticHeadersEntry', (_message.Message,), {
    'DESCRIPTOR' : _CREATEGATEWAYREQUEST_STATICHEADERSENTRY,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.CreateGatewayRequest.StaticHeadersEntry)
    })
  ,

  'TlsConfig' : _reflection.GeneratedProtocolMessageType('TlsConfig', (_message.Message,), {
    'DESCRIPTOR' : _CREATEGATEWAYREQUEST_TLSCONFIG,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.CreateGatewayRequest.TlsConfig)
    })
  ,

  'RetryConfig' : _reflection.GeneratedProtocolMessageType('RetryConfig', (_message.Message,), {
    'DESCRIPTOR' : _CREATEGATEWAYREQUEST_RETRYCONFIG,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.CreateGatewayRequest.RetryConfig)
    })
  ,
  'DESCRIPTOR' : _CREATEGATEWAYREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.CreateGatewayRequest)
  })
_sym_db.RegisterMessage(CreateGatewayRequest)
_sym_db.RegisterMessage(CreateGatewayRequest.StaticHeadersEntry)
_sym_db.RegisterMessage(CreateGatewayRequest.TlsConfig)
_sym_db.RegisterMessage(CreateGatewayRequest.RetryConfig)

InitResponse = _reflection.GeneratedProtocolMessageType('InitResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _INITRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.InitResponse.Error)
    })
  ,
  'DESCRIPTOR' : _INITRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.InitResponse)
  })
_sym_db.RegisterMessage(InitResponse)
_sym_db.RegisterMessage(InitResponse.Error)

CreateWorkerRequest = _reflection.GeneratedProtocolMessageType('CreateWorkerRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEWORKERREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.CreateWorkerRequest)
  })
_sym_db.RegisterMessage(CreateWorkerRequest)

RegisterWorkerResponse = _reflection.GeneratedProtocolMessageType('RegisterWorkerResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _REGISTERWORKERRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.RegisterWorkerResponse.Error)
    })
  ,
  'DESCRIPTOR' : _REGISTERWORKERRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.RegisterWorkerResponse)
  })
_sym_db.RegisterMessage(RegisterWorkerResponse)
_sym_db.RegisterMessage(RegisterWorkerResponse.Error)

PollWorkflowActivationRequest = _reflection.GeneratedProtocolMessageType('PollWorkflowActivationRequest', (_message.Message,), {
  'DESCRIPTOR' : _POLLWORKFLOWACTIVATIONREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.PollWorkflowActivationRequest)
  })
_sym_db.RegisterMessage(PollWorkflowActivationRequest)

PollWorkflowActivationResponse = _reflection.GeneratedProtocolMessageType('PollWorkflowActivationResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _POLLWORKFLOWACTIVATIONRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.PollWorkflowActivationResponse.Error)
    })
  ,
  'DESCRIPTOR' : _POLLWORKFLOWACTIVATIONRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.PollWorkflowActivationResponse)
  })
_sym_db.RegisterMessage(PollWorkflowActivationResponse)
_sym_db.RegisterMessage(PollWorkflowActivationResponse.Error)

PollActivityTaskRequest = _reflection.GeneratedProtocolMessageType('PollActivityTaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _POLLACTIVITYTASKREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.PollActivityTaskRequest)
  })
_sym_db.RegisterMessage(PollActivityTaskRequest)

PollActivityTaskResponse = _reflection.GeneratedProtocolMessageType('PollActivityTaskResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _POLLACTIVITYTASKRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.PollActivityTaskResponse.Error)
    })
  ,
  'DESCRIPTOR' : _POLLACTIVITYTASKRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.PollActivityTaskResponse)
  })
_sym_db.RegisterMessage(PollActivityTaskResponse)
_sym_db.RegisterMessage(PollActivityTaskResponse.Error)

CompleteWorkflowActivationRequest = _reflection.GeneratedProtocolMessageType('CompleteWorkflowActivationRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMPLETEWORKFLOWACTIVATIONREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.CompleteWorkflowActivationRequest)
  })
_sym_db.RegisterMessage(CompleteWorkflowActivationRequest)

CompleteWorkflowActivationResponse = _reflection.GeneratedProtocolMessageType('CompleteWorkflowActivationResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _COMPLETEWORKFLOWACTIVATIONRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.CompleteWorkflowActivationResponse.Error)
    })
  ,
  'DESCRIPTOR' : _COMPLETEWORKFLOWACTIVATIONRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.CompleteWorkflowActivationResponse)
  })
_sym_db.RegisterMessage(CompleteWorkflowActivationResponse)
_sym_db.RegisterMessage(CompleteWorkflowActivationResponse.Error)

CompleteActivityTaskRequest = _reflection.GeneratedProtocolMessageType('CompleteActivityTaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMPLETEACTIVITYTASKREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.CompleteActivityTaskRequest)
  })
_sym_db.RegisterMessage(CompleteActivityTaskRequest)

CompleteActivityTaskResponse = _reflection.GeneratedProtocolMessageType('CompleteActivityTaskResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _COMPLETEACTIVITYTASKRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.CompleteActivityTaskResponse.Error)
    })
  ,
  'DESCRIPTOR' : _COMPLETEACTIVITYTASKRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.CompleteActivityTaskResponse)
  })
_sym_db.RegisterMessage(CompleteActivityTaskResponse)
_sym_db.RegisterMessage(CompleteActivityTaskResponse.Error)

RecordActivityHeartbeatRequest = _reflection.GeneratedProtocolMessageType('RecordActivityHeartbeatRequest', (_message.Message,), {
  'DESCRIPTOR' : _RECORDACTIVITYHEARTBEATREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.RecordActivityHeartbeatRequest)
  })
_sym_db.RegisterMessage(RecordActivityHeartbeatRequest)

RecordActivityHeartbeatResponse = _reflection.GeneratedProtocolMessageType('RecordActivityHeartbeatResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _RECORDACTIVITYHEARTBEATRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.RecordActivityHeartbeatResponse.Error)
    })
  ,
  'DESCRIPTOR' : _RECORDACTIVITYHEARTBEATRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.RecordActivityHeartbeatResponse)
  })
_sym_db.RegisterMessage(RecordActivityHeartbeatResponse)
_sym_db.RegisterMessage(RecordActivityHeartbeatResponse.Error)

RequestWorkflowEvictionRequest = _reflection.GeneratedProtocolMessageType('RequestWorkflowEvictionRequest', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTWORKFLOWEVICTIONREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.RequestWorkflowEvictionRequest)
  })
_sym_db.RegisterMessage(RequestWorkflowEvictionRequest)

RequestWorkflowEvictionResponse = _reflection.GeneratedProtocolMessageType('RequestWorkflowEvictionResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _REQUESTWORKFLOWEVICTIONRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.RequestWorkflowEvictionResponse.Error)
    })
  ,
  'DESCRIPTOR' : _REQUESTWORKFLOWEVICTIONRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.RequestWorkflowEvictionResponse)
  })
_sym_db.RegisterMessage(RequestWorkflowEvictionResponse)
_sym_db.RegisterMessage(RequestWorkflowEvictionResponse.Error)

ShutdownWorkerRequest = _reflection.GeneratedProtocolMessageType('ShutdownWorkerRequest', (_message.Message,), {
  'DESCRIPTOR' : _SHUTDOWNWORKERREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.ShutdownWorkerRequest)
  })
_sym_db.RegisterMessage(ShutdownWorkerRequest)

ShutdownWorkerResponse = _reflection.GeneratedProtocolMessageType('ShutdownWorkerResponse', (_message.Message,), {

  'Error' : _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR' : _SHUTDOWNWORKERRESPONSE_ERROR,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.ShutdownWorkerResponse.Error)
    })
  ,
  'DESCRIPTOR' : _SHUTDOWNWORKERRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.ShutdownWorkerResponse)
  })
_sym_db.RegisterMessage(ShutdownWorkerResponse)
_sym_db.RegisterMessage(ShutdownWorkerResponse.Error)

FetchBufferedLogsRequest = _reflection.GeneratedProtocolMessageType('FetchBufferedLogsRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHBUFFEREDLOGSREQUEST,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.FetchBufferedLogsRequest)
  })
_sym_db.RegisterMessage(FetchBufferedLogsRequest)

FetchBufferedLogsResponse = _reflection.GeneratedProtocolMessageType('FetchBufferedLogsResponse', (_message.Message,), {

  'LogEntry' : _reflection.GeneratedProtocolMessageType('LogEntry', (_message.Message,), {
    'DESCRIPTOR' : _FETCHBUFFEREDLOGSRESPONSE_LOGENTRY,
    '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
    # @@protoc_insertion_point(class_scope:coresdk.bridge.FetchBufferedLogsResponse.LogEntry)
    })
  ,
  'DESCRIPTOR' : _FETCHBUFFEREDLOGSRESPONSE,
  '__module__' : 'temporal.sdk.core.bridge.bridge_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.bridge.FetchBufferedLogsResponse)
  })
_sym_db.RegisterMessage(FetchBufferedLogsResponse)
_sym_db.RegisterMessage(FetchBufferedLogsResponse.LogEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATEGATEWAYREQUEST_STATICHEADERSENTRY._options = None
  _CREATEGATEWAYREQUEST_STATICHEADERSENTRY._serialized_options = b'8\001'
  _LOGLEVEL._serialized_start=4112
  _LOGLEVEL._serialized_end=4211
  _INITTELEMETRYREQUEST._serialized_start=378
  _INITTELEMETRYREQUEST._serialized_end=548
  _CREATEGATEWAYREQUEST._serialized_start=551
  _CREATEGATEWAYREQUEST._serialized_end=1415
  _CREATEGATEWAYREQUEST_STATICHEADERSENTRY._serialized_start=924
  _CREATEGATEWAYREQUEST_STATICHEADERSENTRY._serialized_end=976
  _CREATEGATEWAYREQUEST_TLSCONFIG._serialized_start=978
  _CREATEGATEWAYREQUEST_TLSCONFIG._serialized_end=1083
  _CREATEGATEWAYREQUEST_RETRYCONFIG._serialized_start=1086
  _CREATEGATEWAYREQUEST_RETRYCONFIG._serialized_end=1415
  _INITRESPONSE._serialized_start=1417
  _INITRESPONSE._serialized_end=1508
  _INITRESPONSE_ERROR._serialized_start=1484
  _INITRESPONSE_ERROR._serialized_end=1508
  _CREATEWORKERREQUEST._serialized_start=1511
  _CREATEWORKERREQUEST._serialized_end=2261
  _REGISTERWORKERRESPONSE._serialized_start=2263
  _REGISTERWORKERRESPONSE._serialized_end=2374
  _REGISTERWORKERRESPONSE_ERROR._serialized_start=1484
  _REGISTERWORKERRESPONSE_ERROR._serialized_end=1508
  _POLLWORKFLOWACTIVATIONREQUEST._serialized_start=2376
  _POLLWORKFLOWACTIVATIONREQUEST._serialized_end=2407
  _POLLWORKFLOWACTIVATIONRESPONSE._serialized_start=2410
  _POLLWORKFLOWACTIVATIONRESPONSE._serialized_end=2640
  _POLLWORKFLOWACTIVATIONRESPONSE_ERROR._serialized_start=2586
  _POLLWORKFLOWACTIVATIONRESPONSE_ERROR._serialized_end=2628
  _POLLACTIVITYTASKREQUEST._serialized_start=2642
  _POLLACTIVITYTASKREQUEST._serialized_end=2667
  _POLLACTIVITYTASKRESPONSE._serialized_start=2670
  _POLLACTIVITYTASKRESPONSE._serialized_end=2870
  _POLLACTIVITYTASKRESPONSE_ERROR._serialized_start=2586
  _POLLACTIVITYTASKRESPONSE_ERROR._serialized_end=2628
  _COMPLETEWORKFLOWACTIVATIONREQUEST._serialized_start=2872
  _COMPLETEWORKFLOWACTIVATIONREQUEST._serialized_end=2986
  _COMPLETEWORKFLOWACTIVATIONRESPONSE._serialized_start=2989
  _COMPLETEWORKFLOWACTIVATIONRESPONSE._serialized_end=3124
  _COMPLETEWORKFLOWACTIVATIONRESPONSE_ERROR._serialized_start=1484
  _COMPLETEWORKFLOWACTIVATIONRESPONSE_ERROR._serialized_end=1508
  _COMPLETEACTIVITYTASKREQUEST._serialized_start=3126
  _COMPLETEACTIVITYTASKREQUEST._serialized_end=3208
  _COMPLETEACTIVITYTASKRESPONSE._serialized_start=3210
  _COMPLETEACTIVITYTASKRESPONSE._serialized_end=3333
  _COMPLETEACTIVITYTASKRESPONSE_ERROR._serialized_start=1484
  _COMPLETEACTIVITYTASKRESPONSE_ERROR._serialized_end=1508
  _RECORDACTIVITYHEARTBEATREQUEST._serialized_start=3335
  _RECORDACTIVITYHEARTBEATREQUEST._serialized_end=3414
  _RECORDACTIVITYHEARTBEATRESPONSE._serialized_start=3417
  _RECORDACTIVITYHEARTBEATRESPONSE._serialized_end=3546
  _RECORDACTIVITYHEARTBEATRESPONSE_ERROR._serialized_start=1484
  _RECORDACTIVITYHEARTBEATRESPONSE_ERROR._serialized_end=1508
  _REQUESTWORKFLOWEVICTIONREQUEST._serialized_start=3548
  _REQUESTWORKFLOWEVICTIONREQUEST._serialized_end=3596
  _REQUESTWORKFLOWEVICTIONRESPONSE._serialized_start=3599
  _REQUESTWORKFLOWEVICTIONRESPONSE._serialized_end=3728
  _REQUESTWORKFLOWEVICTIONRESPONSE_ERROR._serialized_start=1484
  _REQUESTWORKFLOWEVICTIONRESPONSE_ERROR._serialized_end=1508
  _SHUTDOWNWORKERREQUEST._serialized_start=3730
  _SHUTDOWNWORKERREQUEST._serialized_end=3753
  _SHUTDOWNWORKERRESPONSE._serialized_start=3755
  _SHUTDOWNWORKERRESPONSE._serialized_end=3866
  _SHUTDOWNWORKERRESPONSE_ERROR._serialized_start=1484
  _SHUTDOWNWORKERRESPONSE_ERROR._serialized_end=1508
  _FETCHBUFFEREDLOGSREQUEST._serialized_start=3868
  _FETCHBUFFEREDLOGSREQUEST._serialized_end=3894
  _FETCHBUFFEREDLOGSRESPONSE._serialized_start=3897
  _FETCHBUFFEREDLOGSRESPONSE._serialized_end=4110
  _FETCHBUFFEREDLOGSRESPONSE_LOGENTRY._serialized_start=3995
  _FETCHBUFFEREDLOGSRESPONSE_LOGENTRY._serialized_end=4110
# @@protoc_insertion_point(module_scope)
