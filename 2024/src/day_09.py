"""Day 9: Disk Fragmenter

OS implementation! I'm sure there is some nicer abstraction we can use
here, but I couldn't think of anything clever.
"""

import os
from dataclasses import dataclass
from textwrap import dedent
from typing import Optional


@dataclass(frozen=True)
class File:
    ID: Optional[int]
    size: int


@dataclass(frozen=True)
class Data:
    disk: list[Optional[int]]
    files: list[File]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    blocks: list[Optional[int]] = []
    files: list[File] = []
    for i, char in enumerate(data):
        ID = (i // 2) if i % 2 == 0 else None
        for _ in range(int(char)):
            blocks.append(ID)
        files.append(File(ID, int(char)))

    return Data(blocks, files)


def part1(data: Data) -> int:
    disk = data.disk

    first_free = 0
    last_data = len(data.disk) - 1

    while first_free < last_data:
        if disk[first_free] is not None:
            first_free += 1
        elif disk[last_data] is None:
            last_data -= 1
            continue
        else:
            disk[first_free] = disk[last_data]
            disk[last_data] = None

    return sum([i * file_id for i, file_id in enumerate(disk) if file_id is not None])


def part2(data: Data) -> int:
    files = data.files

    last_file_ptr = len(files) - 1
    while files[last_file_ptr].ID is None:
        last_file_ptr -= 1
    last_file_id = files[last_file_ptr].ID

    while last_file_id >= 0:
        file_ptr = 0
        while files[file_ptr].ID != last_file_id:
            file_ptr += 1

        free_ptr = 0
        while free_ptr < file_ptr:
            if files[free_ptr].ID is not None or files[free_ptr].size < files[file_ptr].size:
                free_ptr += 1
                continue

            if free_ptr >= file_ptr:
                break

            src = files[file_ptr]
            dst = files[free_ptr]
            if dst.size == src.size:
                files[free_ptr] = src
                files[file_ptr] = dst
            else:
                files[free_ptr] = src
                files[file_ptr] = File(None, src.size)
                files.insert(free_ptr + 1, File(None, dst.size - src.size))
                file_ptr -= 1
            break
        last_file_id -= 1

    block = 0
    total = 0
    for f in files:
        if f.ID is None:
            block += f.size
        else:
            for i in range(block, block + f.size):
                total += i * f.ID
            block += f.size
    return total


def test_part1() -> None:
    data = dedent("""
    2333133121414131402
    """).strip()
    assert part1(parse(data)) == 1928


def test_part2() -> None:
    data = dedent("""
    2333133121414131402
    """).strip()
    assert part2(parse(data)) == 2858


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
