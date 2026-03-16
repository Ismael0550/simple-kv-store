#!/usr/bin/env python3

import os
import sys

DATA_FILE = "data.db"


class KeyValueStore:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.load()

    def find_index(self, key):
        for i in range(len(self.entries)):
            if self.entries[i][0] == key:
                return i
        return -1

    def set_in_memory(self, key, value):
        index = self.find_index(key)
        if index == -1:
            self.entries.append([key, value])
        else:
            self.entries[index][1] = value

    def append_to_file(self, key, value):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"SET {key}\t{value}\n")
            f.flush()
            os.fsync(f.fileno())

    def load(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")

                if not line.startswith("SET "):
                    continue

                content = line[4:]
                parts = content.split("\t", 1)

                if len(parts) != 2:
                    continue

                key, value = parts
                self.set_in_memory(key, value)

    def set(self, key, value):
        self.append_to_file(key, value)
        self.set_in_memory(key, value)

    def get(self, key):
        index = self.find_index(key)
        if index == -1:
            return None
        return self.entries[index][1]


def main():
    store = KeyValueStore(DATA_FILE)

    for raw_line in sys.stdin:
        line = raw_line.strip()

        if not line:
            continue

        if line == "EXIT":
            break

        if line.startswith("SET "):
            parts = line.split(" ", 2)
            if len(parts) < 3:
                print("ERROR", flush=True)
                continue

            key = parts[1]
            value = parts[2]
            store.set(key, value)
            print("OK", flush=True)
            continue

        if line.startswith("GET "):
            parts = line.split(" ", 1)
            if len(parts) != 2 or not parts[1]:
                print("ERROR", flush=True)
                continue

            key = parts[1]
            value = store.get(key)

            if value is None:
                print("NOT FOUND", flush=True)
            else:
                print(value, flush=True)
            continue

        print("ERROR", flush=True)


if __name__ == "__main__":
    main()
