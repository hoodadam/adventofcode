from math import prod

from typing import Optional

DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()


class PacketType:
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


class Packet:
    def __init__(self, version, packet_type, val=None, sub_packets=None):
        # type: (Packet, int, int, Optional[int], Optional[list[Packet]]) -> None
        self.version = version
        self.packet_type = packet_type
        if packet_type == PacketType.LITERAL:
            assert val and not sub_packets
            self.val = val
            self.version_sum = version
        else:
            assert sub_packets and not val
            self.version_sum = self.version + sum(sub_packet.version_sum for sub_packet in sub_packets)
            if packet_type < PacketType.LITERAL:
                if packet_type == PacketType.SUM:
                    func = sum
                elif packet_type == PacketType.PRODUCT:
                    func = prod
                elif packet_type == PacketType.MINIMUM:
                    func = min
                elif packet_type == PacketType.MAXIMUM:
                    func = max
                else:
                    raise AssertionError()
                self.val = func(sub_packet.val for sub_packet in sub_packets)
            else:
                assert len(sub_packets) == 2
                left, right = sub_packets
                if packet_type == PacketType.GREATER_THAN:
                    self.val = int(left.val > right.val)
                elif packet_type == PacketType.LESS_THAN:
                    self.val = int(left.val < right.val)
                elif packet_type == PacketType.EQUAL_TO:
                    self.val = int(left.val == right.val)
                else:
                    raise AssertionError()


def parse_packet(packet_str):
    hex_ints = [int(c, base=16) for c in packet_str]
    bits = [(hex_int // (1 << (3 - i))) % 2 == 1 for hex_int in hex_ints for i in range(4)]

    cursor = 0

    def _parse_internal():
        # type: () -> Packet
        def _parse_int(length):
            # type: (int) -> int
            result = 0
            nonlocal cursor
            for _ in range(length):
                result *= 2
                result += bits[cursor]
                cursor += 1
            return result

        def _parse_bool():
            # type: () -> bool
            nonlocal cursor
            result = bits[cursor]
            cursor += 1
            return result

        def _parse_literal():
            # type: () -> int
            read_on = _parse_bool()
            total = _parse_int(4)
            while read_on:
                read_on = _parse_bool()
                total *= 16
                total += _parse_int(4)
            return total

        version = _parse_int(3)
        packet_type = _parse_int(3)
        if packet_type == PacketType.LITERAL:
            val = _parse_literal()
            return Packet(version, packet_type, val=val)
        else:
            len_type = _parse_bool()
            if len_type:
                num_packets = _parse_int(11)
                sub_packets = [_parse_internal() for _ in range(num_packets)]
                return Packet(version, packet_type, sub_packets=sub_packets)
            else:
                num_bits = _parse_int(15)
                cursor_limit = cursor + num_bits
                sub_packets = []
                while cursor < cursor_limit:
                    sub_packets.append(_parse_internal())
                assert cursor == cursor_limit
                return Packet(version, packet_type, sub_packets=sub_packets)

    return _parse_internal()


for line in raw_data.splitlines():
    packet = parse_packet(line)
    print(f'Version sum: {packet.version_sum}; Value: {packet.val}')
