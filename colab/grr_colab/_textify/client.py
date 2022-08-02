#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Module that contains converters of client values into human readable text."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time

from typing import Text


def last_seen(last_ping: int) -> Text:
  """Constructs last seen label from last ping time.

  Args:
    last_ping: Last ping time in microseconds.

  Returns:
    Constructed last seen label.
  """
  current_time_secs = time.time()
  last_ping_secs = last_ping / 10**6
  last_seen_secs = abs(current_time_secs - last_ping_secs)

  if last_seen_secs < 60:
    measure_unit = 'seconds'
    measure_value = int(last_seen_secs)
  elif last_seen_secs < 60 * 60:
    measure_unit = 'minutes'
    measure_value = int(last_seen_secs / 60)
  elif last_seen_secs < 60 * 60 * 24:
    measure_unit = 'hours'
    measure_value = int(last_seen_secs / (60 * 60))
  else:
    measure_unit = 'days'
    measure_value = int(last_seen_secs / (60 * 60 * 24))

  if current_time_secs >= last_ping_secs:
    return f'{measure_value} {measure_unit} ago'
  else:
    return f'in {measure_value} {measure_unit}'


def online_icon(last_ping: int) -> Text:
  current_time_secs = time.time()
  last_seen_secs = current_time_secs - last_ping / 10**6

  if last_seen_secs < 60 * 15:
    return '🌕'
  elif last_seen_secs < 60 * 60 * 24:
    return '🌓'
  else:
    return '🌑'


def online_status(last_ping: int) -> Text:
  current_time_secs = time.time()
  last_seen_secs = current_time_secs - last_ping / 10**6

  if last_seen_secs < 60 * 15:
    return 'online'
  elif last_seen_secs < 60 * 60 * 24:
    return 'seen-1d'
  else:
    return 'offline'


def mac(packed_bytes: bytes) -> Text:
  return (':'.join(
      '{:02x}'.format(b) for b in packed_bytes) if packed_bytes else '')
