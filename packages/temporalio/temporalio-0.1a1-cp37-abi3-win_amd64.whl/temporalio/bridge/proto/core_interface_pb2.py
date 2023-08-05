# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/sdk/core/core_interface.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from temporalio.bridge.proto.activity_result import activity_result_pb2 as temporal_dot_sdk_dot_core_dot_activity__result_dot_activity__result__pb2
from temporalio.bridge.proto.activity_task import activity_task_pb2 as temporal_dot_sdk_dot_core_dot_activity__task_dot_activity__task__pb2
from temporalio.bridge.proto.common import common_pb2 as temporal_dot_sdk_dot_core_dot_common_dot_common__pb2
from temporalio.bridge.proto.external_data import external_data_pb2 as temporal_dot_sdk_dot_core_dot_external__data_dot_external__data__pb2
from temporalio.bridge.proto.workflow_activation import workflow_activation_pb2 as temporal_dot_sdk_dot_core_dot_workflow__activation_dot_workflow__activation__pb2
from temporalio.bridge.proto.workflow_commands import workflow_commands_pb2 as temporal_dot_sdk_dot_core_dot_workflow__commands_dot_workflow__commands__pb2
from temporalio.bridge.proto.workflow_completion import workflow_completion_pb2 as temporal_dot_sdk_dot_core_dot_workflow__completion_dot_workflow__completion__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&temporal/sdk/core/core_interface.proto\x12\x07\x63oresdk\x1a\x1egoogle/protobuf/duration.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x37temporal/sdk/core/activity_result/activity_result.proto\x1a\x33temporal/sdk/core/activity_task/activity_task.proto\x1a%temporal/sdk/core/common/common.proto\x1a\x33temporal/sdk/core/external_data/external_data.proto\x1a?temporal/sdk/core/workflow_activation/workflow_activation.proto\x1a;temporal/sdk/core/workflow_commands/workflow_commands.proto\x1a?temporal/sdk/core/workflow_completion/workflow_completion.proto\"Q\n\x11\x41\x63tivityHeartbeat\x12\x12\n\ntask_token\x18\x01 \x01(\x0c\x12(\n\x07\x64\x65tails\x18\x02 \x03(\x0b\x32\x17.coresdk.common.Payload\"n\n\x16\x41\x63tivityTaskCompletion\x12\x12\n\ntask_token\x18\x01 \x01(\x0c\x12@\n\x06result\x18\x02 \x01(\x0b\x32\x30.coresdk.activity_result.ActivityExecutionResultb\x06proto3')



_ACTIVITYHEARTBEAT = DESCRIPTOR.message_types_by_name['ActivityHeartbeat']
_ACTIVITYTASKCOMPLETION = DESCRIPTOR.message_types_by_name['ActivityTaskCompletion']
ActivityHeartbeat = _reflection.GeneratedProtocolMessageType('ActivityHeartbeat', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVITYHEARTBEAT,
  '__module__' : 'temporal.sdk.core.core_interface_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.ActivityHeartbeat)
  })
_sym_db.RegisterMessage(ActivityHeartbeat)

ActivityTaskCompletion = _reflection.GeneratedProtocolMessageType('ActivityTaskCompletion', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVITYTASKCOMPLETION,
  '__module__' : 'temporal.sdk.core.core_interface_pb2'
  # @@protoc_insertion_point(class_scope:coresdk.ActivityTaskCompletion)
  })
_sym_db.RegisterMessage(ActivityTaskCompletion)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACTIVITYHEARTBEAT._serialized_start=538
  _ACTIVITYHEARTBEAT._serialized_end=619
  _ACTIVITYTASKCOMPLETION._serialized_start=621
  _ACTIVITYTASKCOMPLETION._serialized_end=731
# @@protoc_insertion_point(module_scope)
