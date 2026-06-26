PROTO_SRC := protos
GO_OUT := protos_go
PY_OUT := protos_python

.PHONY: all models writer clean

all: models writer

# Models — shared data structures (Go + Python)
models:
	protoc \
		--proto_path=$(PROTO_SRC) \
		--go_out=$(GO_OUT) \
		--go_opt=paths=source_relative \
		$(PROTO_SRC)/models/*.proto
	protoc \
		--proto_path=$(PROTO_SRC) \
		--python_out=$(PY_OUT) \
		--pyi_out=$(PY_OUT) \
		$(PROTO_SRC)/models/*.proto

# Writer — gRPC service (Go only)
writer:
	protoc \
		--proto_path=$(PROTO_SRC) \
		--go_out=$(GO_OUT) \
		--go_opt=paths=source_relative \
		--go-grpc_out=$(GO_OUT) \
		--go-grpc_opt=paths=source_relative \
		$(PROTO_SRC)/writer/*.proto

clean:
	rm -rf $(GO_OUT)/models/*.pb.go
	rm -rf $(GO_OUT)/writer/*.pb.go $(GO_OUT)/writer/*_grpc.pb.go
	rm -rf $(PY_OUT)/models/*_pb2.py $(PY_OUT)/models/*_pb2.pyi
