# Simple Key-Value Store

EUID: IKS0010

## Description
This project implements a simple persistent key-value store with the following commands:

- `SET <key> <value>`
- `GET <key>`
- `EXIT`

The database uses append-only storage in `data.db`. On startup, the program replays the log to rebuild the in-memory index.

## Features
- Command-line interface using STDIN and STDOUT
- Immediate persistence to disk after every write
- Recovery after restart
- Custom in-memory index using a list, not a built-in dictionary
- Last write wins semantics

## How to Run
```bash
python3 kv_store.py
