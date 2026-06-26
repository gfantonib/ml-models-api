module ml-models-api/services/gateway

go 1.23

require (
	google.golang.org/grpc v1.72.1
	google.golang.org/protobuf v1.36.6
	ml-models-api/protos/protos_go v0.0.0-00010101000000-000000000000
)

replace ml-models-api/protos/protos_go => ../../protos/protos_go
