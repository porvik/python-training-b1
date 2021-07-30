import glob
import os
import struct

class Debug():
    global_log_level = 1

    def __init__(self, level=None):
        self.level = level if level else 0

    def __call__(self, wrapped_function):
        def wrapper_function(*args, **kwargs):
            if Debug.global_log_level <= self.level:
                print("[DEBUG] Called {}".format(locals()))
                print("[DEBUG] Called {}".format(wrapped_function))
            return wrapped_function(*args, **kwargs)
        return wrapper_function


class InputDataset():
    def __init__(self, file_path):
        self.file_obj = open(file_path, 'rb')
        self.file_size = os.stat(file_path).st_size

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file_obj.close()

    def __gt__(self, other):
        if other < self.file_size:
            return True
        else:
            return False


class Reader():
    @Debug()
    def _unpack_int(self, raw):
        return struct.unpack('i', raw)[0]

    @Debug()
    def _unpack_str(self, raw):
        return struct.unpack('4s', raw)[0].decode('utf-8')

    @Debug()
    def _unpack_double(self, raw):
        return struct.unpack('f', raw)[0]

    @Debug()
    def read_files(self, pattern, packet_structure):
        fields = [
            attribute.attrib for attribute in packet_structure.header.attribute
        ]
        fields.extend([
            variable.attrib for variable in packet_structure.payload.variable
        ])
        all_packets = []
        packet_count = 0
        for entry in glob.glob(pattern):
            packet_offset = 0
            with InputDataset(entry) as input_dataset:
                print(input_dataset)
                while packet_offset < input_dataset:
                    packet_count += 1
                    if packet_count == 4:
                        break
                    single_packet = []
                    for field in fields:
                        field_offset = packet_offset + int(field['offset'])
                        field_size = int(field['size'])
                        input_dataset.file_obj.seek(field_offset)
                        raw = input_dataset.file_obj.read(field_size)
                        if hasattr(self, '_unpack_{}'.format(field['type'])):
                            value = getattr(self, '_unpack_{}'.format(field['type']))(raw)
                        else:
                            value = struct.unpack('B', raw)[0]
                        single_packet.append({
                            'name': field['name'],
                            'value': value
                        })
                    packet_offset += int(fields[-1]['offset']) + int(fields[-1]['size'])
                    all_packets.append(single_packet)
        return all_packets
