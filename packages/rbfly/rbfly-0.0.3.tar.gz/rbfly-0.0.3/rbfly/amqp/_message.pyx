#
# rbfly - a library for RabbitMQ Streams using Python asyncio
#
# Copyright (C) 2021-2022 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# language_level=3

"""
Codec for AMQP 1.0 messages.

Why custom codec:

    >>> import proton
    >>> proton.VERSION
    (0, 35, 0)
    >>> %timeit proton.Message(body='abcd').encode()
    13.2 µs ± 31.6 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

    >>> import uamqp
    >>> uamqp.__version__
    '1.4.3'
    >>> %timeit uamqp.Message(body='abcd').encode_message()
    6.63 µs ± 45.1 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

    >>> from rbfly.amqp._message import Message, encode_amqp
    >>> buff = bytearray(1024)
    >>> %timeit encode_amqp(buff, Message(b'abcd'))
    113 ns ± 3.31 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

RbFly codec adds little overhead to basic, binary message, which allows to
use AMQP 1.0 by default for all use cases.
"""

import array
import cython
import logging
from cpython cimport array, PyUnicode_CheckExact, PyBytes_CheckExact, \
    PyBool_Check, PyLong_CheckExact, PyFloat_CheckExact, PyDict_Check

from libc.stdint cimport int16_t, int32_t, int64_t, uint8_t, uint16_t, \
    uint32_t, uint64_t
from libc.string cimport memcpy

from .._codec cimport pack_uint32, pack_uint64, pack_double, \
    unpack_uint16, unpack_uint32, unpack_uint64, unpack_float, unpack_double
from ..types import AMQPBody

logger = logging.getLogger(__name__)

DEF DESCRIPTOR_START = 0x00
DEF DESCRIPTOR_MESSAGE_BINARY = 0x75
DEF DESCRIPTOR_MESSAGE_VALUE = 0x77

DEF TYPE_BINARY_SHORT = 0xa0
DEF TYPE_BINARY_LONG = 0xb0
DEF TYPE_STRING_SHORT = 0xa1
DEF TYPE_STRING_LONG = 0xb1

DEF BOOL_TRUE = 0x41
DEF BOOL_FALSE = 0x42

DEF TYPE_UBYTE = 0x50
DEF TYPE_USHORT = 0x60
DEF TYPE_UINT = 0x70
DEF TYPE_SMALLUINT = 0x52
DEF TYPE_UINT0 = 0x43
DEF TYPE_ULONG = 0x80
DEF TYPE_SMALLULONG = 0x53
DEF TYPE_ULONG0 = 0x44

DEF TYPE_BYTE = 0x51
DEF TYPE_SHORT = 0x61
DEF TYPE_INT = 0x71
DEF TYPE_SMALLINT = 0x54
DEF TYPE_LONG = 0x81
DEF TYPE_SMALLLONG = 0x55

DEF TYPE_FLOAT = 0x72
DEF TYPE_DOUBLE = 0x82

DEF TYPE_MAP8 = 0xc1
DEF TYPE_MAP32 = 0xd1

DEF MESSAGE_OPAQUE_BINARY = (TYPE_SMALLULONG << 8) | DESCRIPTOR_MESSAGE_BINARY
DEF MESSAGE_VALUE = (TYPE_SMALLULONG << 8) | DESCRIPTOR_MESSAGE_VALUE

@cython.no_gc_clear
@cython.final
@cython.freelist(1000)
cdef class Message:
    def __cinit__(self, object body, *, int stream_offset=0, float stream_timestamp=0):
        self.body = body

        self.stream_offset = stream_offset
        self.stream_timestamp = stream_timestamp

    def __eq__(self, other: Message):
        return self.body == other.body \
            and self.stream_offset == other.stream_offset \
            and self.stream_timestamp == other.stream_timestamp

    def __repr__(self) -> str:
        if isinstance(self.body, (bytes, str)) and len(self.body) > 10:
            ext = b'...' if isinstance(self.body, bytes) else '...'
            value = self.body[:10] + ext
        else:
            value = self.body
        return 'Message(body={!r}, stream_offset={}, stream_timestamp={})'.format(
            value,
            self.stream_offset,
            self.stream_timestamp,
        )

def encode_amqp(buffer: bytearray, message: Message) -> int:
    return c_encode_amqp(<char*> buffer, message)

def decode_amqp(char *buffer) -> Message:
    return c_decode_amqp(buffer)

# TODO: double check the size of each parsed value
cdef Message c_decode_amqp(char *buffer):
    cdef:
        uint32_t desc_code
        uint8_t type_code
        object body
        Py_ssize_t size
        Py_ssize_t offset = 0

    desc_code = unpack_uint32(&buffer[offset])
    offset += sizeof(uint32_t)

    type_code = desc_code & 0xff
    desc_code = desc_code >> 8

    if desc_code == MESSAGE_OPAQUE_BINARY:
        if type_code == TYPE_BINARY_SHORT:
            size = buffer[offset]
            offset += 1
            body = _decode_strb(&buffer[offset], size, type_code)
        elif type_code == TYPE_BINARY_LONG:
            size = unpack_uint32(&buffer[offset])
            offset += sizeof(uint32_t)
            body = _decode_strb(&buffer[offset], size, type_code)
        else:
            body = None
            logger.warning(
                'cannot decode message for descriptor 0x{:06x} and type code 0x{:02x}'
                .format(desc_code, type_code)
            )
    elif desc_code == MESSAGE_VALUE:
        body = _decode_value(buffer, type_code, &offset)
    else:
        body = None
        logger.warning(
            'cannot decode message for descriptor 0x{:06x}'.format(desc_code)
        )

    return Message(body)

cdef inline object _decode_value(char *buffer, uint8_t type_code, Py_ssize_t *offset_start):
    cdef:
        object body
        Py_ssize_t size
        Py_ssize_t offset = offset_start[0]

    if type_code == TYPE_STRING_LONG:
        size = unpack_uint32(&buffer[offset])
        offset += sizeof(uint32_t)
        body = _decode_strb(&buffer[offset], size, type_code)
        offset += size
    elif type_code == TYPE_STRING_SHORT:
        size = buffer[offset]
        offset += 1
        body = _decode_strb(&buffer[offset], size, type_code)
        offset += size
    elif type_code in (BOOL_TRUE, BOOL_FALSE):
         body = type_code == BOOL_TRUE
    elif type_code in (TYPE_UINT0, TYPE_ULONG0):
        body = 0
    elif type_code in (TYPE_UBYTE, TYPE_SMALLUINT, TYPE_SMALLULONG):
        body = <unsigned char> buffer[offset]
        offset += 1
    elif type_code == TYPE_USHORT:
        body = unpack_uint16(&buffer[offset])
        offset += sizeof(uint16_t)
    elif type_code == TYPE_UINT:
        body = <uint32_t> unpack_uint32(&buffer[offset])
        offset += sizeof(uint32_t)
    elif type_code == TYPE_ULONG:
        body = <uint64_t> unpack_uint64(&buffer[offset])
        offset += sizeof(uint64_t)
    elif type_code in (TYPE_BYTE, TYPE_SMALLINT, TYPE_SMALLLONG):
        body = <signed char> buffer[offset]
        offset += 1
    elif type_code == TYPE_SHORT:
        body = <int16_t> unpack_uint16(&buffer[offset])
        offset += sizeof(int16_t)
    elif type_code == TYPE_INT:
        body = <int32_t> unpack_uint32(&buffer[offset])
        offset += sizeof(int32_t)
    elif type_code == TYPE_LONG:
        body = <int64_t> unpack_uint64(&buffer[offset])
        offset += sizeof(int64_t)
    elif type_code == TYPE_FLOAT:
        body = unpack_float(&buffer[offset])
        offset += sizeof(float)
    elif type_code == TYPE_DOUBLE:
        body = unpack_double(&buffer[offset])
        offset += sizeof(double)
    elif type_code == TYPE_MAP32:
        body = _decode_map(buffer, &offset)
    else:
        body = None
        logger.warning('cannot decode message for type_code: 0x{:08x}'.format(type_code))

    offset_start[0] = offset

    return body

cdef inline dict _decode_map(char *buffer, Py_ssize_t *offset_start):
    """
    Decode AMQP map object.
    """
    cdef:
        object key, value
        uint8_t type_code
        Py_ssize_t i
        uint32_t size, dict_len

        dict result = {}
        Py_ssize_t offset = offset_start[0]

    size = unpack_uint32(&buffer[offset])
    offset += sizeof(uint32_t)

    dict_len = unpack_uint32(&buffer[offset])
    offset += sizeof(uint32_t)
    if dict_len % 2 == 1:
        logger.warning('amqp map invalid length: %d'.format(dict_len))
        return None

    for i in range(0, dict_len, 2):
        type_code = buffer[offset]
        offset += 1
        key = _decode_value(buffer, type_code, &offset)

        type_code = buffer[offset]
        offset += 1
        value = _decode_value(buffer, type_code, &offset)

        result[key] = value

    offset_start[0] = offset
    return result

cdef inline object _decode_strb(char *buffer, Py_ssize_t size, uint32_t type_code):
    if type_code % 2 == 1:
        return buffer[0:size].decode('utf-8')
    else:
        return <bytes> buffer[0:size]

cdef Py_ssize_t c_encode_amqp(char *buffer, object message) except -1:
    cdef:
        Py_ssize_t offset = 0
        Py_ssize_t size
        object body = (<Message> message).body

    if PyBytes_CheckExact(body):
        size = len(body)

        offset += _encode_descriptor(&buffer[offset], DESCRIPTOR_MESSAGE_BINARY)
        offset += _encode_strb(
            &buffer[offset],
            body, size,
            TYPE_BINARY_SHORT, TYPE_BINARY_LONG
        )
    else:
        offset += _encode_descriptor(&buffer[offset], DESCRIPTOR_MESSAGE_VALUE)
        offset += _encode_value(&buffer[offset], body)

    return offset

cdef inline Py_ssize_t _encode_dict(char *buffer, object value) except -1:
    """
    Encode Python dictionary into AMQP format.
    """
    cdef:
        object k, v
        Py_ssize_t i
        Py_ssize_t offset = 0
        Py_ssize_t offset_size

    buffer[offset] = TYPE_MAP32
    offset += 1
    offset_size = offset

    # gap for the length of the buffer of an encoded dictionary
    offset += sizeof(uint32_t)

    # number of map elements (both keys and values)
    pack_uint32(&buffer[offset], len(value) * 2)
    offset += sizeof(uint32_t)

    for k, v in value.items():
        offset += _encode_value(&buffer[offset], k)
        offset += _encode_value(&buffer[offset], v)

    # encode the buffer length taken by the dictionary
    pack_uint32(&buffer[offset_size], offset - offset_size)

    return offset

cdef inline Py_ssize_t _encode_value(char *buffer, object value) except -1:
    """
    Encode Python object into AMQP format.
    """
    cdef:
        Py_ssize_t offset = 0
        object value_bin

    if PyUnicode_CheckExact(value):
        value_bin = value.encode('utf-8')
        size = len(value_bin)

        offset += _encode_strb(
            &buffer[offset],
            value_bin,
            size,
            TYPE_STRING_SHORT,
            TYPE_STRING_LONG
        )
    elif PyBool_Check(value):
        buffer[offset] = BOOL_TRUE if value else BOOL_FALSE
        offset += 1
    elif PyLong_CheckExact(value):
        if -2 ** 31 <= value < 2 ** 31:
            buffer[offset] = TYPE_INT
            offset += 1

            pack_uint32(&buffer[offset], <int32_t> value)
            offset += sizeof(int32_t)
        elif -2 ** 63 <= value < 2 ** 63:
            buffer[offset] = TYPE_LONG
            offset += 1

            pack_uint64(&buffer[offset], <int64_t> value)
            offset += sizeof(int64_t)
        elif 2 ** 63 <= value < 2 ** 64:
            buffer[offset] = TYPE_ULONG
            offset += 1

            pack_uint64(&buffer[offset], <uint64_t> value)
            offset += sizeof(uint64_t)
        else:
            raise TypeError('Cannot encode message with value: {}'.format(value))
    elif PyFloat_CheckExact(value):
        buffer[offset] = TYPE_DOUBLE
        offset += 1

        pack_double(&buffer[offset], value)
        offset += sizeof(double)
    elif PyDict_Check(value):
        offset += _encode_dict(&buffer[offset], value)
    else:
        raise TypeError('Cannot encode message with body of type: {}'.format(type(value)))

    return offset

cdef inline Py_ssize_t _encode_descriptor(char *buffer, unsigned char code):
    """
    Encode start of AMQP descriptor.

    :param buffer: Start of the buffer.
    :param code: AMQP descriptor code.
    """
    buffer[0] = DESCRIPTOR_START
    buffer[1] = TYPE_SMALLULONG
    buffer[2] = code
    return 3

cdef inline Py_ssize_t _encode_strb(
        char *buffer,
        char *body,
        Py_ssize_t size,
        unsigned char code_short,
        unsigned char code_long,
    ) except -1:

    cdef Py_ssize_t offset = 0

    if size < 256:
        buffer[offset] = code_short
        offset += 1
        buffer[offset] = size
        offset += 1
    elif size < 2 ** 32:
        buffer[offset] = code_long
        offset += 1
        pack_uint32(&buffer[offset], size)
        offset += 4
    else:
        raise ValueError('Data too long, size={}'.format(size))

    memcpy(&buffer[offset], <char*> body, size)
    return offset + size

# vim: sw=4:et:ai
