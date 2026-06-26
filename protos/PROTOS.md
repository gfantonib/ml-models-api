# Protos

Shared protobuf definitions used by all services.

## Structure

```
protos/
├── protos/
│   ├── trigger.proto              ← trigger enums and message
│   └── models/
│       ├── ant_colony.proto       ← ANT_COLONY_MODEL messages
│       └── pythagorean.proto      ← PYTHAGOREAN_SUPPORT_MACHINE_MODEL messages
├── protos_go/                     ← generated Go code
│   ├── trigger.pb.go
│   └── models/
│       ├── ant_colony.pb.go
│       └── pythagorean.pb.go
├── protos_python/                 ← generated Python code
│   ├── trigger_pb2.py
│   ├── trigger_pb2.pyi
│   └── models/
│       ├── ant_colony_pb2.py
│       ├── ant_colony_pb2.pyi
│       ├── pythagorean_pb2.py
│       └── pythagorean_pb2.pyi
└── PROTOS.md
```

## Prerequisites

```bash
# protoc compiler (>= 3.20 for --pyi_out)
brew install protobuf

# Go plugin
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
```

## Generate

Run from the `protos/` directory:

```bash
make all      # generate Go + Python
make go       # generate Go only
make python   # generate Python only
make clean    # remove generated files
```
