#!/usr/bin/env python
"""GRR Colab API errors."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Text, List, Optional

from grr_colab import flags
from grr_response_proto import jobs_pb2

FLAGS = flags.FLAGS


class UnknownClientError(Exception):

  def __init__(self, client_id: Text, cause: Exception) -> None:
    self.client_id = client_id
    self.cause = cause
    msg = f'Client with id {client_id} does not exist: {cause}'
    super(UnknownClientError, self).__init__(msg)


class AmbiguousHostnameError(Exception):

  def __init__(self, hostname: Text, clients: List[Text]) -> None:
    self.hostname = hostname
    self.clients = clients
    msg = f'Too many clients ({clients}) found for hostname: {hostname}'
    super(AmbiguousHostnameError, self).__init__(msg)


class UnknownHostnameError(Exception):

  def __init__(self, hostname: Text) -> None:
    self.hostname = hostname
    msg = f'No clients found for hostname: {hostname}'
    super(UnknownHostnameError, self).__init__(msg)


class ApprovalMissingError(Exception):

  def __init__(self, client_id: Text, cause: Exception) -> None:
    self.client_id = client_id
    self.cause = cause
    msg = f'No approval to the client {client_id} found: {cause}'
    super(ApprovalMissingError, self).__init__(msg)


class FlowTimeoutError(Exception):
  """Raised if a flow is timed out.

  Attributes:
    client_id: Id of the client.
    flow_id: Id of the flow.
    cause: Exception raised.
  """

  def __init__(self,
               client_id: Text,
               flow_id: Text,
               cause: Optional[Exception] = None) -> None:
    self.client_id = client_id
    self.flow_id = flow_id
    self.cause = cause

    msg = f'Flow with id {flow_id} is timed out'
    url = self._build_path_to_ui()
    if url is not None:
      msg = f'{msg}. Results will be available at {url} when the flow finishes'
    super(FlowTimeoutError, self).__init__(msg)

  def _build_path_to_ui(self) -> Optional[Text]:
    if not FLAGS.grr_admin_ui_url:
      return None
    url = '{}/#/clients/{}/flows/{}'
    return url.format(FLAGS.grr_admin_ui_url, self.client_id, self.flow_id)


class NotDirectoryError(Exception):

  def __init__(self, client_id: Text, path: Text) -> None:
    self.client_id = client_id
    self.path = path
    msg = f'Path `{client_id}` for client {path} is not a directory'
    super(NotDirectoryError, self).__init__(msg)


class UnsupportedPathTypeError(Exception):

  def __init__(self, path_type: jobs_pb2.PathSpec.PathType) -> None:
    self.path_type = path_type
    msg = f'Unsupported path type {path_type}'
    super(UnsupportedPathTypeError, self).__init__(msg)
