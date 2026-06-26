package handler

import (
	pb "ml-models-api/protos/protos_go/writer"
)

type Handler struct {
	writer pb.WriterClient
}

func NewHandler(writer pb.WriterClient) *Handler {
	return &Handler{writer: writer}
}
