import json
import struct

import brotli as brotli

wsBinaryHeaderList = [
    {"name": "Header Length", "key": "headerLen", "bytes": 2, "offset": 4, "value": 16},
    {"name": "Protocol Version", "key": "ver", "bytes": 2, "offset": 6, "value": 1},
    {"name": "Operation", "key": "op", "bytes": 4, "offset": 8, "value": 1},
    {"name": "Sequence Id", "key": "seq", "bytes": 4, "offset": 12, "value": 1}
]


def get_encoder():
    # Note: In Python 3, there's no need for a custom TextEncoder
    # because the default string encode() method provides this functionality.
    return {"encode": lambda t: t.encode('utf-8')}


def merge_array_buffers(buf1, buf2):
    return buf1 + buf2


def encode_data(message, value):
    if not hasattr(encode_data, "encoder"):
        encode_data.encoder = get_encoder()

    header = bytearray(16)
    encoded_message = encode_data.encoder["encode"](message)

    # Setting the header length
    struct.pack_into("!I", header, 0, 16 + len(encoded_message))

    # Setting the operation value
    wsBinaryHeaderList[2]["value"] = value

    # Setting other headers
    for h in wsBinaryHeaderList:
        if h["bytes"] == 4:
            struct.pack_into("!I", header, h["offset"], h["value"])
        elif h["bytes"] == 2:
            struct.pack_into("!H", header, h["offset"], h["value"])

    return merge_array_buffers(header, encoded_message)


def get_int32(buffer, offset=0, little_endian=False):
    # buffer should be a bytes-like object
    format_string = '<i' if little_endian else '>i'
    return struct.unpack_from(format_string, buffer, offset)[0]


def get_int16(buffer, offset=0, little_endian=False):
    format_string = '<h' if little_endian else '>h'
    return struct.unpack_from(format_string, buffer, offset)[0]


def convert_to_object(data):
    result = {'body': []}
    result['packetLen'] = struct.unpack_from('>i', data, 0)[0]

    # Extract headers based on wsBinaryHeaderList
    for item in wsBinaryHeaderList:
        if item['bytes'] == 4:
            result[item['key']] = get_int32(data, item['offset'])
        elif item['bytes'] == 2:
            result[item['key']] = get_int16(data, item['offset'])
            result[item['key']] = struct.unpack_from('>H', data, item['offset'])[0]

    if result['packetLen'] < len(data):
        convert_to_object(data[:result['packetLen']])

    if not result.get('op') or result['op'] not in [5, 8]:
        if result.get('op') and result['op'] == 3:
            result['body'] = {'count': struct.unpack_from('>I', data, 16)[0]}
    else:
        i = 0
        while i < len(data):
            s = struct.unpack_from('>I', data, i)[0]
            a = struct.unpack_from('>H', data, i + 4)[0]

            try:
                parsed = None
                if result['ver'] == 0:
                    decoded_data = data[i + a: i + s].decode()
                    parsed = json.loads(decoded_data) if decoded_data else None
                elif result['ver'] == 3:
                    decompressed = brotli.decompress(data[i + a: i + s])
                    parsed = convert_to_object(decompressed)['body']
                if parsed:
                    result['body'].append(parsed)
            except Exception as e:
                print("decode body error:", e)

            i += s

    return result

# t = '{"uid":3537111630219964,"roomid":23167843,"protover":3,"buvid":"498A93D9-462A-9C6B-6D8A-E4C12100A30C32999infoc","platform":"web","type":2,"key":"Hu6HurBlQNaHsq0tpwWAuV7k024sls6-4ilD94wpX7QYkuDoXdqPRbjSGy492wNw3xqXU0rZRn70vsdw58PBVGJcNbp-_aiEXxCz9RBiF0gtW4Bxk7Cg7ECMdXX5ypvxwrTGI7-vvLha3LBP3Ar3mEG_CDxflgs="}'
#
# print(a(t,7))
