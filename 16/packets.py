from __future__ import annotations
from typing import Final, List


class Packet:
    def __init__(self, packet: str) -> None:
        self.packet = packet
        self.contains: None | List[Packet] = None

        self.packet = self.packet[:len(self)]

    def version(self) -> str:
        return self.packet[:3]

    def type(self) -> str:
        return self.packet[3:6]

    def is_literal(self) -> bool:
        return self.type() == "100"

    def __len__(self) -> int:
        length = len(self.version()) + len(self.type())
        if self.is_literal():
            while True:
                group = self.packet[length:length + 5]
                length += 5
                if group[0] == "1":
                    continue
                return length
        else:
            length += 1 + self.length_section_length()
            length += sum([len(c) for c in self.children()])
            return length

    def length_section_length(self) -> int:
        if self.is_literal():
            raise Exception("Literal package misused")
        return 11 if self.packet[6] == "1" else 15

    def children_length(self) -> int:
        section = self.packet[7:7 + self.length_section_length()]
        return int(section, 2)

    def length_in_bits(self) -> bool:
        return self.length_section_length() == 15

    def length_in_packets(self) -> bool:
        return not self.length_in_bits()

    def children_section(self) -> str:
        return self.packet[7 + self.length_section_length():]

    def children(self) -> List[Packet]:
        if self.contains is not None:
            return self.contains

        children_bits = self.children_section()
        children: List[Packet] = []
        if self.length_in_bits():
            children_bits = children_bits[:self.children_length()]

        while True:
            p = Packet(children_bits)
            children_bits = children_bits[len(p):]  # 11
            children.append(p)

            if self.length_in_bits():
                if not len(children_bits):
                    break
            if self.length_in_packets():
                if self.children_length() == len(children):
                    break

        self.contains = children
        return children

    def value(self) -> int:
        if not self.is_literal():
            raise Exception("Operator package misused")

        value_bits = self.packet[len(self.version()) + len(self.type()):]
        number = ""
        while True:
            group = value_bits[:5]
            value_bits = value_bits[5:]
            number += group[1:]
            if group[0] == "0":
                break
        return int(number, 2)

    def version_sum(self) -> int:
        version = int(self.version(), 2)
        if self.is_literal():
            return version
        else:
            return version + sum([c.version_sum() for c in self.children()])

    def __repr__(self) -> str:
        return self.packet


def packets(input: str) -> None:
    input_content: Final = open(input).readline().strip()

    packet_value: Final = int(input_content, base=16)
    leading_zeros: Final = (4 - len(f"{int(input_content[0], base=16):b}"))
    packet_repr: Final = f"{'0' * leading_zeros}{packet_value:b}"

    print(f"Added up version numbers give {Packet(packet_repr).version_sum()}")


if __name__ == "__main__":
    packets("input")
